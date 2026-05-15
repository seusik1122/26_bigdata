# LLM으로 HTTP 요청 분류하기 - 프롬프트 실험

실험일: 2026-05-15  
모델: gemma3:4b (Ollama 로컬 실행)  
데이터: CSIC 2010 HTTP Dataset에서 100건 샘플 (정상 47, 공격 53)

---

## 프롬프트 전략

프롬프트를 어떻게 짜느냐에 따라 정확도가 달라지는지 확인해보려고 4가지로 나눠서 실험했다.

- **A. 2-shot Basic** : 예시 2개만 보여주는 기본 형태
- **B. 5-shot Multi-attack** : SQL Injection, XSS, Path Traversal, Command Injection 등 다양한 공격 유형 예시 5개
- **C. Chain-of-Thought** : "단계별로 생각해봐" 방식. Parse → Pattern → Decision 순으로 추론하게 함
- **D. Rule-hint + 5-shot** : 탐지해야 할 키워드 목록(예: `' OR`, `<script>`, `../`) 힌트를 주고 예시 5개

---

## 프롬프트 원문 예시

아래는 `GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1` 요청을 분류할 때 실제로 보낸 프롬프트다.

### A. 2-shot Basic

```
You are a web security expert. Classify each HTTP request as "Normal" or "Anomalous" and provide a brief reason.

Examples:
Request: GET /index.jsp HTTP/1.1
Output: {"label": "Normal", "reason": "Standard page request, no suspicious pattern"}

Request: GET /search?q=' OR '1'='1 HTTP/1.1
Output: {"label": "Anomalous", "reason": "Classic SQL Injection pattern with OR 1=1"}

Now classify:
Request: GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1
Output:
```

### B. 5-shot Multi-attack

```
You are a web security expert. Classify the HTTP request as "Normal" or "Anomalous".
Respond ONLY with valid JSON: {"label": "...", "reason": "..."}

### Examples
Request: GET /tienda1/publico/index.jsp HTTP/1.1
Output: {"label": "Normal", "reason": "Regular page navigation, no attack indicators"}

Request: GET /search?q=1' OR '1'='1 HTTP/1.1
Output: {"label": "Anomalous", "reason": "SQL Injection via OR-based tautology"}

Request: GET /page?name=<script>alert(1)</script> HTTP/1.1
Output: {"label": "Anomalous", "reason": "XSS: injected <script> tag in parameter"}

Request: GET /files?path=../../etc/passwd HTTP/1.1
Output: {"label": "Anomalous", "reason": "Path Traversal: ../.. to access /etc/passwd"}

Request: POST /upload HTTP/1.1
Body: filename=shell.php&cmd=ls
Output: {"label": "Anomalous", "reason": "Command Injection via cmd parameter"}

### Classify this
Request: GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1
Output:
```

### C. Chain-of-Thought

```
You are a web security analyst. Think step by step before classifying.

### Example
Request: GET /search?q=1' OR '1'='1 HTTP/1.1
Step 1 - Parse: URL parameter q contains single quotes and OR keyword.
Step 2 - Pattern: OR-based tautology is classic SQL Injection.
Step 3 - Decision: Anomalous.
Output: {"label": "Anomalous", "reason": "SQL Injection via OR tautology in q param"}

...

Now analyze step by step and output JSON only:
Request: GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1
Output:
```

### D. Rule-hint + 5-shot

```
You are a web security expert. Classify HTTP requests as "Normal" or "Anomalous".

### Attack indicators to look for:
- SQL Injection: ' OR, UNION SELECT, 1=1, --, ;DROP
- XSS: <script>, onerror=, javascript:, alert(
- Path Traversal: ../, %2e%2e, /etc/passwd, /windows/system32
- Command Injection: ;ls, |whoami, `id`, %0a
- Encoding evasion: %27 (single quote), %3c (< ), %00 (null byte)

### Examples
(... 5개 예시 ...)

### Classify
Request: GET /tienda1/publico/anadir.jsp?id=2'+OR+'1'='1 HTTP/1.1
Output:
```

---

## 결과

| 전략 | 정확도 | F1 | 소요 시간 | 건당 시간 |
|------|--------|-----|-----------|-----------|
| A. 2-shot Basic | 0.8400 | **0.8519** ★ | 73.4초 | 0.73초 |
| B. 5-shot Multi-attack | 0.8500 | 0.8454 | 57.9초 | 0.58초 |
| C. Chain-of-Thought | 0.8200 | 0.8421 | 131.7초 | 1.32초 |
| D. Rule-hint + 5-shot | 0.8300 | 0.8317 | 60.8초 | 0.61초 |

F1 기준으로는 A(2-shot Basic)가 0.8519로 제일 높게 나왔다.  
예시를 더 많이 넣는다고 꼭 성능이 오르는 건 아니었다.

---

## 오분류 사례 분석

A 프롬프트 기준으로 16건이 틀렸는데, 크게 두 가지 패턴이었다.

**1. 정상인데 공격으로 잘못 판단 (오탐)**  
파라미터가 많거나 특수문자(é, í 같은 유럽 문자)가 들어간 정상 요청을 공격으로 봤다.  
예: `password=Bu7c2Pié` → "unusual characters, potential attack" 으로 판단

**2. 공격인데 정상으로 잘못 판단 (미탐)**  
겉보기에 평범한 요청인데 실제론 공격인 경우를 못 잡았다.  
예: `GET /busytime.nsf` → 평범한 파일 요청처럼 보여서 Normal 판단

