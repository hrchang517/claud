# 용어집 (Glossary)

> 출처: http://minzkn.com/vibecoding/pages/glossary.html
> AI, LLM, CLI, MCP 등 Vibe Coding과 AI 개발에 필요한 모든 기술 용어를 A-Z 알파벳 순으로 정리한 종합 사전입니다.

## 📖 이 용어집에 대하여

이 용어집은 AI 기반 개발(Vibe Coding)을 처음 접하는 초보자부터 숙련된 개발자까지 모두를 위한 참고 자료입니다. 각 용어는 명확한 정의와 함께 관련 페이지 링크를 제공하여 깊이 있는 학습을 돕습니다.

## 핵심 개념 관계도

AI Vibe Coding 생태계의 핵심 용어들이 어떻게 연결되는지 한눈에 파악할 수 있는 개념 관계도입니다.

- **핵심 개념**: LLM(대규모 언어 모델), Transformer(기반 아키텍처), Token(처리 단위), Prompt(사용자 입력/지시), API(프로그래밍 인터페이스), Context Window(최대 입력 범위)
- **AI Vibe Coding 도구**: Claude CLI(코드 생성/편집), Cursor(IDE AI 어시스턴트), MCP(데이터 소스 연결), Ollama(로컬 LLM 실행), RAG(검색 증강 생성)
- **관련 개념**: Agent, Fine-tuning, Tool Use, Embedding, Vector DB

---

## A

### Agent (에이전트)
특정 작업을 자율적으로 수행하는 AI 프로그램. LLM을 기반으로 목표를 설정하고, 계획을 세우며, 도구를 사용하여 작업을 완수합니다. 예를 들어, AutoGPT는 사용자가 목표만 제시하면 스스로 단계를 나누어 실행하는 에이전트입니다.
*관련 페이지: MCP 소개, Tool Use 소개*

### Aider
Git 통합을 강조한 오픈소스 AI CLI 코딩 도구. 파일 변경 사항을 자동으로 커밋하고, 여러 LLM(Claude, GPT, Ollama 등)을 지원합니다. Python 기반이며 `pip install aider-chat`로 설치합니다.
*관련 페이지: Aider 가이드, CLI 도구 비교*

### Anthropic (앤트로픽)
Claude를 개발한 AI 연구 기업. OpenAI 출신 연구진들이 2021년 설립하였으며, AI 안전성과 해석 가능성(Interpretability)에 중점을 둡니다. Claude 모델 계열(고성능/균형형/경량형)을 제공합니다.
*관련 페이지: Vibe Coding이란?, Claude CLI*

### API (Application Programming Interface)
소프트웨어 간 통신을 위한 인터페이스. LLM 서비스는 REST API 또는 SDK를 통해 프로그래밍 방식으로 접근할 수 있습니다. 예: Claude API, OpenAI API, Gemini API.
*관련 페이지: API 키 관리, 다중 LLM 전환*

### AutoGPT
사용자가 고수준 목표를 제시하면 AI가 스스로 계획을 세우고 반복 실행하는 자율 에이전트 프레임워크. 웹 검색, 파일 읽기/쓰기, 코드 실행 등 다양한 도구를 활용하여 복잡한 작업을 자동화합니다.
*관련 페이지: AI CLI 도구 생태계*

### AVX2 (Advanced Vector Extensions 2)
Intel/AMD CPU의 고급 SIMD 명령어 세트. 로컬 LLM(Ollama, LM Studio)을 실행할 때 AVX2 지원 여부가 성능에 큰 영향을 미칩니다. 2013년 이후 대부분의 데스크톱/노트북 CPU는 AVX2를 지원합니다.
*관련 페이지: Ollama 소개, 로컬 LLM 가이드*

## B

### Backpropagation (역전파)
신경망 학습에서 출력 오차를 입력 방향으로 전파하며 가중치를 업데이트하는 알고리즘. LLM의 사전 학습(Pre-training)과 미세 조정(Fine-tuning) 단계에서 핵심적인 역할을 합니다.
*관련 페이지: LLM 기초*

### Batch API (배치 API)
다수의 요청을 한 번에 처리하는 API. 비용이 저렴하지만 응답 시간이 길어집니다(수 시간 소요 가능). 대량의 텍스트 분류, 번역, 요약 작업에 적합합니다.
*관련 페이지: Batch API 활용*

### Benchmark (벤치마크)
모델의 성능을 측정하는 표준 테스트. MMLU(다분야 이해), HumanEval(코딩), GSM8K(수학) 등이 대표적입니다. 벤치마크 점수만으로 실제 성능을 완벽히 판단할 수는 없으므로 직접 테스트가 중요합니다.
*관련 페이지: LLM 모델 비교*

### BERT (Bidirectional Encoder Representations from Transformers)
Google이 2018년 발표한 양방향 Transformer 기반 언어 모델. 텍스트의 맥락을 양방향으로 학습하여 이해력이 뛰어납니다. 최신 LLM(GPT, Claude)의 기초가 된 중요한 모델입니다.
*관련 페이지: 모델 패밀리*

## C

### Cache (캐시)
이전 요청의 결과를 저장하여 재사용함으로써 응답 속도를 높이고 비용을 절감하는 기술. Claude는 Prompt Caching 기능을 제공하여 반복되는 긴 컨텍스트(문서, 코드베이스)를 캐시합니다.
*관련 페이지: 프롬프트 캐싱*

### Chain-of-Thought (사고 사슬)
LLM이 복잡한 문제를 단계별로 추론하도록 유도하는 프롬프팅 기법. "단계별로 생각해봐" 같은 지시를 통해 정확도를 높입니다. 수학 문제, 논리 퍼즐, 코드 디버깅에 효과적입니다.

```
# 일반 프롬프트 (오답 가능)
"17 × 24는?"

# CoT 프롬프트 (정확도 향상)
"17 × 24를 계산해줘. 단계별로 생각해봐:
1. 17 × 20 = ?
2. 17 × 4 = ?
3. 두 결과를 더하면?"
```
*관련 페이지: 프롬프트 고급 기법*

### ChatGPT (챗GPT)
OpenAI가 개발한 대화형 AI 서비스. 다양한 GPT 계열 및 추론 계열 모델을 제공하며, 웹 인터페이스와 API를 통해 이용 가능합니다. 2022년 11월 출시 이후 전 세계적으로 가장 널리 사용되는 AI 어시스턴트입니다.
*관련 페이지: LLM 모델 비교, Vibe Coding이란?*

### Claude (클로드)
Anthropic이 개발한 LLM 시리즈. Claude는 긴 컨텍스트와 안정적인 코드 생성 품질로 Vibe Coding에서 널리 사용됩니다. Vibe Coding에서 가장 많이 사용되는 모델 중 하나입니다.
*관련 페이지: Claude CLI, Claude CLI 5분 시작*

### Codex
OpenAI의 코딩 에이전트. 코드베이스를 읽고 수정하며, 테스트 실행과 문서화를 자동화하는 워크플로우에 사용됩니다. CLI/IDE/웹 환경에서 작업을 수행할 수 있으며, 안전한 권한 제어와 리뷰 절차가 중요합니다.
*관련 페이지: Codex 가이드, OpenAI API, CLI 모범 사례*

### CLI (Command Line Interface, 명령줄 인터페이스)
텍스트 명령어로 프로그램을 제어하는 인터페이스. AI CLI 도구(Claude CLI, Aider, Continue 등)는 터미널에서 자연어로 코드를 생성하고 수정합니다. GUI보다 자동화와 스크립팅에 유리합니다.
*관련 페이지: AI CLI 도구 생태계, CLI 도구 비교*

### Cline
VS Code 확장으로 제공되는 AI 코딩 어시스턴트. 이전에는 Claude Dev로 알려졌으며, 파일 편집, 터미널 명령 실행, 웹 검색 등을 수행합니다. Claude, GPT, Ollama 등 여러 LLM을 지원합니다.
*관련 페이지: Cline 가이드, CLI 도구 비교*

### Context (컨텍스트)
LLM이 처리할 수 있는 입력 텍스트의 범위. 컨텍스트 창(Context Window)이 클수록 더 긴 문서, 대화, 코드베이스를 한 번에 처리할 수 있습니다. 정확한 한도는 모델/버전별로 다르므로 공식 모델 문서를 기준으로 확인해야 합니다.
*관련 페이지: 컨텍스트 관리, 토큰 최적화*

### Continue.dev (컨티뉴)
오픈소스 AI 코딩 어시스턴트. VS Code와 JetBrains IDE에서 작동하며, 자동완성, 인라인 편집, 채팅 인터페이스를 제공합니다. 로컬 LLM(Ollama) 및 클라우드 LLM을 모두 지원합니다.
*관련 페이지: Continue.dev 가이드*

### Copilot (GitHub Copilot)
GitHub와 OpenAI가 공동 개발한 AI 코딩 어시스턴트. VS Code, Visual Studio, JetBrains IDE에서 코드 자동완성과 제안을 제공합니다. 월 변동(개인) 또는 변동(프로) 구독 모델입니다.
*관련 페이지: AI CLI 도구 생태계*

### CUDA (Compute Unified Device Architecture)
NVIDIA GPU에서 병렬 연산을 수행하는 플랫폼. 로컬 LLM을 실행할 때 CUDA 지원 GPU가 있으면 CPU 대비 수십 배 빠른 추론이 가능합니다. Ollama, LM Studio, LocalAI 모두 CUDA를 지원합니다.
*관련 페이지: GPU 가속, Ollama 소개*

### Cursor
AI 기능이 통합된 코드 에디터(VS Code 포크). 자연어로 코드를 생성하고, 파일 전체를 리팩토링하며, 프로젝트 전반을 이해하는 능력이 뛰어납니다. 플랜/한도/과금 정책은 시점에 따라 달라질 수 있으므로 공식 가격 페이지 확인이 필요합니다.
*관련 페이지: Cursor 가이드, CLI 도구 비교*

## D

### DeepSeek
중국 기반의 오픈소스 LLM. DeepSeek Coder는 코드 생성에 특화되어 있으며, Ollama를 통해 로컬에서 실행할 수 있습니다. 벤치마크 성능은 모델 크기, 학습 데이터, 추론 설정에 따라 달라집니다.
*관련 페이지: Ollama 모델 가이드*

### Deployment (배포)
개발한 애플리케이션을 실제 사용자가 접근할 수 있도록 프로덕션 환경에 올리는 과정. Vibe Coding으로 생성한 코드는 Docker, Vercel, AWS, GCP 등 다양한 플랫폼에 배포할 수 있습니다.
*관련 페이지: CI/CD & LLM*

### Docker (도커)
애플리케이션을 컨테이너로 패키징하여 어디서나 동일하게 실행할 수 있도록 하는 플랫폼. 로컬 LLM 서버(Ollama, LocalAI)를 Docker로 실행하면 환경 설정이 간편합니다.
*관련 페이지: Docker 설정*

### Dotfiles (닷파일)
Unix/Linux 시스템에서 점(.)으로 시작하는 설정 파일. `.bashrc`, `.zshrc`, `.gitconfig` 등이 대표적입니다. AI CLI 도구 설정 파일(`.aider.conf.yml`, `.continue/config.json`)도 닷파일입니다.
*관련 페이지: LLM 개발 환경*

## E

### Embedding (임베딩)
텍스트를 고차원 벡터로 변환한 수치 표현. 의미적으로 유사한 텍스트는 비슷한 벡터 값을 가집니다. RAG(Retrieval-Augmented Generation)에서 문서 검색에 활용됩니다.

```python
from openai import OpenAI
import numpy as np

client = OpenAI()
def get_embedding(text: str) -> list[float]:
    res = client.embeddings.create(input=text, model="text-embedding-3-small")
    return res.data[0].embedding  # 1536차원 벡터

# 코사인 유사도로 문서 검색
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```
*관련 페이지: RAG 소개*

### Environment Variable (환경 변수)
운영체제에서 프로세스에 전달되는 키-값 쌍. API 키를 환경 변수(`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)로 저장하면 코드에 하드코딩하지 않아도 됩니다. 보안과 이식성을 높입니다.
*관련 페이지: API 키 관리*

### Epoch (에포크)
전체 학습 데이터셋을 한 번 학습하는 단위. 모델이 3 epoch 학습했다면 전체 데이터를 3번 반복하여 학습한 것입니다. Fine-tuning 시 적절한 epoch 설정이 과적합(Overfitting)을 방지하는 열쇠입니다.
*관련 페이지: Fine-tuning 가이드*

## F

### Falcon
Technology Innovation Institute(UAE)가 개발한 오픈소스 LLM. Falcon-7B, Falcon-40B 등이 있으며, 상업적 사용이 가능합니다. Ollama를 통해 로컬에서 실행할 수 있습니다.
*관련 페이지: Ollama 모델 가이드*

### Few-shot (퓨샷 학습)
몇 개의 예시만으로 모델이 새로운 작업을 수행하도록 하는 학습 방식. 프롬프트에 2-3개의 예시를 포함하면 원하는 형식의 출력을 얻을 수 있습니다. Zero-shot보다 정확하지만 One-shot보다 토큰 소비가 많습니다.
*관련 페이지: 프롬프트 고급 기법*

### Fine-tuning (미세 조정)
사전 학습된 모델을 특정 작업이나 도메인에 맞게 추가 학습시키는 과정. 커스텀 데이터셋으로 Fine-tuning하면 특화된 성능을 얻을 수 있습니다. OpenAI, Claude는 Fine-tuning API를 제공합니다.
*관련 페이지: Fine-tuning 가이드*

### Function Calling (함수 호출)
LLM이 외부 함수나 API를 호출하여 실시간 데이터를 가져오거나 작업을 수행하는 기능. 예를 들어, "오늘 날씨는?" 질문에 날씨 API를 호출하여 답합니다. Tool Use, Function Tool이라고도 불립니다.
*관련 페이지: Tool Use 소개, MCP 소개*

## G

### Gemini (제미니)
Google이 개발한 멀티모달 LLM. Gemini 모델 계열은 텍스트, 이미지, 비디오, 오디오를 함께 처리할 수 있습니다. 무료 티어(하루 15 요청)를 제공합니다.
*관련 페이지: LLM 모델 비교*

### GGUF (Georgi Gerganov Unified Format)
Georgi Gerganov가 개발한 llama.cpp 프로젝트의 로컬 LLM 모델 포맷. GGML(구 포맷)을 계승하여 2023년 8월에 등장했으며, 모델 가중치, 토크나이저, 하이퍼파라미터, 아키텍처 메타데이터를 단일 파일에 모두 포함하는 자기 설명적(self-describing) 바이너리 포맷입니다. mmap(메모리 매핑)을 통한 즉시 로딩, Q2_K~Q8_0 등 다양한 양자화 내장 지원, 크로스 플랫폼 호환이 핵심 특징입니다. Ollama, LM Studio, llama.cpp, GPT4All 등 대부분의 로컬 LLM 런타임이 GGUF를 표준 포맷으로 채택하고 있습니다.
*관련 페이지: GGUF 상세 가이드, 파일 내부 구조, 양자화 동작 원리, GPU 오프로딩, 양자화 가이드*

### Git (깃)
분산 버전 관리 시스템. Aider는 Git과 긴밀히 통합되어 AI가 생성한 코드를 자동으로 커밋합니다. Vibe Coding에서도 Git을 사용하여 변경 사항을 추적하고 롤백할 수 있습니다.
*관련 페이지: Aider 가이드, LLM 개발 환경*

### GitHub (깃허브)
Git 저장소 호스팅 플랫폼. GitHub Copilot, GitHub Actions 등 개발 도구를 제공하며, 오픈소스 커뮤니티의 중심지입니다. AI CLI 도구들의 코드도 대부분 GitHub에 공개되어 있습니다.
*관련 페이지: AI CLI 도구 생태계*

### GPT (Generative Pre-trained Transformer)
OpenAI가 개발한 LLM 시리즈. GPT 계열과 추론 특화 계열을 제공하며, 범용 언어 이해와 생성 능력이 뛰어납니다. ChatGPT와 API를 통해 제공됩니다.
*관련 페이지: LLM 모델 비교*

### GPU (Graphics Processing Unit)
병렬 연산에 최적화된 프로세서. LLM 추론과 학습에서 CPU 대비 수십~수백 배 빠릅니다. NVIDIA GPU(CUDA)가 가장 널리 사용되며, Apple Silicon(Metal), AMD(ROCm)도 지원됩니다.
*관련 페이지: GPU 가속, 하드웨어 가이드*

## H

### Haiku (하이쿠)
Claude 모델 시리즈 중 경량/고속 티어를 가리키는 명칭. 일반적으로 낮은 비용과 빠른 응답 속도가 장점이며, 간단한 작업에 적합합니다. 일반적으로 대형 모델보다 비용 효율적인 선택지로 사용됩니다.
*관련 페이지: LLM 모델 비교*

### Hallucination (환각)
LLM이 사실이 아닌 정보를 그럴듯하게 생성하는 현상. 예를 들어, 존재하지 않는 논문을 인용하거나 잘못된 코드를 자신 있게 제시합니다. RAG, 검증 프롬프트, 신뢰도 점수 등으로 완화할 수 있습니다.

```
# 나쁜 예 — 환각 유발
"양자컴퓨터의 최신 연구 동향을 알려줘"

# 좋은 예 — 출처 기반 답변 요구
"아래 논문 요약을 바탕으로만 답변해줘.
모르는 것은 '정보 없음'이라고 해줘.
[논문 요약: ...]"

# 좋은 예 — 불확실성 명시 요청
"확실하지 않은 정보는 '확인 필요'로 표시해줘"
```
*관련 페이지: 프롬프트 모범 사례*

### HTTP (HyperText Transfer Protocol)
웹에서 데이터를 주고받는 프로토콜. LLM API는 대부분 HTTP REST API 형태로 제공되며, POST 요청으로 프롬프트를 전송하고 응답을 받습니다.
*관련 페이지: API 기초*

### Hugging Face (허깅페이스)
오픈소스 AI 커뮤니티 플랫폼. 수만 개의 사전 학습 모델, 데이터셋, 데모 앱을 제공합니다. Transformers 라이브러리는 LLM을 쉽게 사용할 수 있는 Python 패키지입니다.
*관련 페이지: 로컬 LLM 가이드*

## I

### IDE (Integrated Development Environment, 통합 개발 환경)
코드 작성, 디버깅, 빌드를 하나의 환경에서 수행하는 도구. VS Code, JetBrains IDE, Cursor 등이 있으며, AI 확장 프로그램을 통해 Vibe Coding을 지원합니다.
*관련 페이지: LLM 개발 환경*

### In-context Learning (문맥 내 학습)
모델 파라미터를 변경하지 않고, 프롬프트에 예시를 포함하여 새로운 작업을 수행하도록 하는 방식. Few-shot, Zero-shot 학습이 모두 In-context Learning에 속합니다.
*관련 페이지: 프롬프트 고급 기법*

### Inference (추론)
학습된 모델을 사용하여 새로운 입력에 대한 출력을 생성하는 과정. LLM API 요청은 모두 추론 과정입니다. 추론 속도는 토큰/초(Tokens per Second)로 측정됩니다.
*관련 페이지: 성능 최적화*

## J

### JSON-RPC
JSON 형식으로 원격 프로시저 호출(RPC)을 수행하는 프로토콜. MCP(Model Context Protocol)가 JSON-RPC를 기반으로 작동하며, 클라이언트와 서버 간 메시지를 주고받습니다.
*관련 페이지: MCP 소개, MCP 구현*

### JWT (JSON Web Token)
인증 정보를 안전하게 전송하기 위한 토큰 표준. API 키 대신 JWT를 사용하여 사용자 인증을 구현할 수 있습니다. 헤더, 페이로드, 서명으로 구성됩니다.
*관련 페이지: API 키 관리*

## K

### Key Management (키 관리)
API 키, 비밀번호 등 민감한 정보를 안전하게 저장하고 사용하는 방법. 환경 변수, `.env` 파일, 키 관리 서비스(AWS KMS, Azure Key Vault)를 활용합니다. 절대 코드에 하드코딩하거나 Git에 커밋하지 마세요.
*관련 페이지: API 키 관리*

### Kubernetes (쿠버네티스)
컨테이너 오케스트레이션 플랫폼. 로컬 LLM 서버를 여러 노드에 분산 배포하거나, AI 서비스를 스케일링할 때 사용합니다. K8s로 줄여 부르기도 합니다.
*관련 페이지: 배포 전략*

## L

### LangChain (랭체인)
LLM 애플리케이션을 구축하기 위한 Python/JavaScript 프레임워크. 프롬프트 템플릿, 체인, 에이전트, 메모리 등을 모듈화하여 복잡한 LLM 워크플로우를 쉽게 구현합니다.
*관련 페이지: LangChain RAG 구현, 에이전트 프레임워크*

### LiteLLM
여러 LLM API를 통합하여 동일한 인터페이스로 사용할 수 있게 하는 Python 라이브러리. Claude, GPT, Gemini, Mistral 등을 하나의 함수로 호출합니다. 비용 최적화와 Fallback 전략에 유용합니다.
*관련 페이지: 다중 LLM 전환*

### LLM (Large Language Model, 대규모 언어 모델)
수억~수조 개의 파라미터를 가진 신경망 기반 언어 모델. GPT, Claude, Gemini, LLaMA 등이 있으며, 텍스트 이해와 생성 능력이 뛰어납니다. Vibe Coding의 핵심 기술입니다.
*관련 페이지: LLM 기초, Vibe Coding이란?*

### LlamaIndex
LLM을 위한 데이터 프레임워크. RAG(Retrieval-Augmented Generation)를 쉽게 구현할 수 있으며, 문서 로딩, 인덱싱, 검색을 자동화합니다. 이전에는 GPT Index로 알려졌습니다.
*관련 페이지: LlamaIndex RAG*

### LocalAI
OpenAI API 호환 로컬 서버. Ollama, llama.cpp 등의 백엔드를 사용하여 로컬에서 LLM을 실행하면서도 OpenAI SDK를 그대로 사용할 수 있습니다. Docker로 간편히 설치할 수 있습니다.
*관련 페이지: 로컬 LLM 가이드*

### LoRA (Low-Rank Adaptation)
효율적인 Fine-tuning 기법. 전체 모델을 재학습하는 대신 작은 어댑터 레이어만 학습하여 메모리와 시간을 절약합니다. 수백 MB의 LoRA 파일로 수십 GB 모델을 커스터마이징할 수 있습니다.
*관련 페이지: Fine-tuning 가이드*

## M

### MCP (Model Context Protocol)
LLM과 외부 도구/데이터소스를 연결하는 표준 프로토콜. Anthropic이 개발했으며, 파일 시스템, 데이터베이스, API 등을 LLM이 직접 사용할 수 있게 합니다. JSON-RPC 기반이며 클라이언트-서버 구조입니다.
*관련 페이지: MCP 소개, MCP 구현*

### Metal
Apple의 GPU 가속 프레임워크. M1/M2/M3 칩을 탑재한 Mac에서 Ollama, LM Studio가 Metal을 사용하여 로컬 LLM을 빠르게 실행합니다. CUDA의 Apple Silicon 버전이라고 볼 수 있습니다.
*관련 페이지: GPU 가속, Ollama 소개*

### Mistral (미스트랄)
프랑스 기반의 오픈소스 LLM. Mistral 7B, Mixtral 8x7B 등이 있으며, 작은 크기 대비 높은 성능으로 유명합니다. Ollama를 통해 로컬에서 실행 가능하며, API도 제공됩니다.
*관련 페이지: Ollama 모델 가이드, LLM 모델 비교*

### Model (모델)
학습된 신경망의 파라미터와 구조. GPT 계열, Claude 계열, Gemini 계열 등이 모두 모델입니다. 모델 크기는 파라미터 수(7B, 70B, 175B 등)로 표현됩니다.
*관련 페이지: LLM 기초*

### Modelfile
Ollama에서 커스텀 모델을 정의하는 설정 파일. 베이스 모델, 시스템 프롬프트, 파라미터(temperature, top_p 등)를 지정합니다. Dockerfile과 유사한 문법을 사용합니다.
*관련 페이지: Modelfile 가이드*

### Multimodal (멀티모달)
텍스트, 이미지, 오디오, 비디오 등 여러 종류의 데이터를 처리할 수 있는 모델. 멀티모달 모델은 이미지 내용을 이해하고 설명할 수 있습니다.
*관련 페이지: LLM 모델 비교*

## N

### Neural Network (신경망)
인간의 뇌 구조를 모방한 기계학습 모델. 여러 층의 뉴런(노드)이 연결되어 있으며, 입력 데이터를 처리하여 출력을 생성합니다. LLM은 Transformer 구조의 심층 신경망(Deep Neural Network)입니다.
*관련 페이지: LLM 기초*

### Node.js (노드)
JavaScript 런타임 환경. 서버 사이드 JavaScript 실행이 가능하며, npm을 통해 수많은 패키지를 사용할 수 있습니다. Claude Code의 현재 권장 설치 경로는 네이티브 설치이며, npm 설치는 호환성 목적의 deprecated 경로입니다.
*관련 페이지: LLM 개발 환경*

### NPM (Node Package Manager)
Node.js 패키지 관리자. `npm install`로 라이브러리를 설치하고, `npx`로 패키지를 설치 없이 실행합니다. Claude Code는 과거 npm/npx 방식도 쓰였지만, 현재 공식 문서는 네이티브 설치를 우선 권장합니다.
*관련 페이지: Claude CLI 5분 시작*

### NVIDIA (엔비디아)
GPU 제조사. CUDA를 통해 AI/ML 가속에서 압도적인 점유율을 가지고 있습니다. RTX 4090, A100, H100 등이 LLM 학습과 추론에 널리 사용됩니다.
*관련 페이지: 하드웨어 가이드*

## O

### o 시리즈 (OpenAI o3/o4-mini)
OpenAI의 추론 특화 모델군. 긴 사고 과정을 거쳐 복잡한 문제를 해결하며, 수학, 과학, 코딩 벤치마크에서 높은 점수를 기록합니다. o1은 레거시 모델로 보고, 신규 구현에서는 o3/o4-mini 또는 GPT-5.4 계열을 우선 검토하세요.
*관련 페이지: LLM 모델 비교*

### Ollama (올라마)
로컬 LLM을 쉽게 실행할 수 있는 오픈소스 도구. `ollama run llama3` 한 줄로 모델을 다운로드하고 실행합니다. Docker처럼 간단하며, Mac/Linux/Windows를 모두 지원합니다.
*관련 페이지: Ollama 소개, Ollama 로컬 시작*

### OpenAI (오픈AI)
ChatGPT와 GPT 시리즈를 개발한 AI 연구 기업. 언어/음성/이미지 분야의 다양한 모델과 개발 도구를 제공하며, AI 대중화에 큰 기여를 했습니다.
*관련 페이지: LLM 모델 비교*

### OpenCode
터미널 중심의 오픈소스 AI 코딩 에이전트. TUI/CLI와 IDE 연동을 통해 코드 생성, 수정, 실행 보조를 제공합니다. OpenCode Zen과 연결하면 코딩 작업용으로 검증된 모델 조합을 사용할 수 있습니다.
*관련 페이지: OpenCode 가이드*

### Opus (오퍼스)
Claude 모델 라인업에서 고성능 티어를 가리키는 명칭. 복잡한 추론과 고난도 작업에 유리하지만 일반적으로 비용이 높습니다.
*관련 페이지: LLM 모델 비교*

## P

### Parameter (파라미터)
신경망에서 학습되는 가중치(Weight)와 편향(Bias). LLM의 크기는 파라미터 수로 표현되며, 7B(70억), 70B(700억), 175B(1750억) 등이 있습니다. 파라미터가 많을수록 성능이 좋지만 메모리와 연산 비용이 증가합니다.
*관련 페이지: LLM 기초*

### Portkey
여러 LLM API를 통합 관리하는 플랫폼. 하나의 API로 Claude, GPT, Gemini 등을 호출하고, 사용량 모니터링, 캐싱, Fallback 등을 지원합니다. 비용 최적화와 안정성 향상에 유용합니다.
*관련 페이지: 다중 LLM 전환*

### PostgreSQL (포스트그레SQL)
오픈소스 관계형 데이터베이스. pgvector 확장을 통해 임베딩 벡터를 저장하고 검색할 수 있어 RAG 시스템에 자주 사용됩니다.
*관련 페이지: pgvector 연동 예제*

### Pre-training (사전 학습)
대규모 텍스트 데이터셋으로 모델을 학습하는 초기 단계. GPT, Claude 등은 인터넷의 수조 개 토큰으로 사전 학습되었습니다. 사전 학습 후 Fine-tuning으로 특정 작업에 맞게 조정합니다.
*관련 페이지: LLM 기초*

### Prompt (프롬프트)
LLM에게 전달하는 입력 텍스트. 질문, 지시, 예시 등을 포함할 수 있으며, 프롬프트의 품질이 출력 품질을 결정합니다. Vibe Coding에서는 자연어 프롬프트로 코드를 생성합니다.
*관련 페이지: 프롬프트 기본, 코딩용 프롬프트*

### Python SDK
Python으로 LLM API를 쉽게 사용할 수 있는 라이브러리. `pip install anthropic`, `pip install openai`로 설치합니다. REST API보다 편리하며 타입 힌트를 제공합니다.
*관련 페이지: API 기초*

## Q

### Quantization (양자화)
모델의 가중치를 32비트에서 8비트, 4비트로 줄여 메모리와 연산량을 감소시키는 기법. GGUF 포맷은 양자화된 모델을 효율적으로 저장합니다. 4비트 양자화로 70B 모델을 40GB → 10GB로 줄일 수 있습니다.
*관련 페이지: 양자화 가이드, Ollama 소개*

### Query (쿼리)
데이터베이스나 검색 엔진에 보내는 요청. RAG 시스템에서는 사용자 질문을 벡터로 변환하여 관련 문서를 쿼리합니다.
*관련 페이지: 검색 전략*

### Qwen (치웬)
Alibaba가 개발한 오픈소스 LLM. Qwen 2.5, Qwen Coder 등이 있으며, 중국어와 영어에서 높은 성능을 보입니다. Ollama를 통해 로컬에서 실행할 수 있습니다.
*관련 페이지: Ollama 모델 가이드*

## R

### RAG (Retrieval-Augmented Generation)
외부 문서를 검색하여 LLM에게 제공함으로써 최신 정보나 특정 도메인 지식을 활용하는 기법. 환각(Hallucination)을 줄이고 정확도를 높입니다. 벡터 데이터베이스, 임베딩, 검색 알고리즘을 조합합니다.

```python
import anthropic

def rag_answer(query: str, docs: list[str]) -> str:
    # 1. 검색: 쿼리와 관련 문서 선택 (간단 버전 — 실제는 벡터 유사도)
    context = "\n\n".join(docs[:3])

    # 2. 증강: 컨텍스트를 포함한 프롬프트 구성
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-5", max_tokens=1024,
        system=f"다음 문서를 기반으로 답변하세요:\n{context}",
        messages=[{"role": "user", "content": query}],
    )
    return response.content[0].text
```
*관련 페이지: RAG 소개*

### Rate Limiting (요청 제한)
API 서비스가 과도한 요청을 방지하기 위해 시간당 요청 횟수를 제한하는 것. Claude API는 분당 요청 수(RPM), 분당 토큰 수(TPM)로 제한합니다. 429 에러가 발생하면 재시도 로직을 구현해야 합니다.
*관련 페이지: API 모범 사례*

### Redis (레디스)
인메모리 데이터베이스. 캐시, 세션 저장, 임베딩 벡터 저장(RediSearch)에 사용됩니다. 빠른 응답 속도가 필요한 RAG 시스템에서 자주 활용됩니다.
*관련 페이지: RAG 캐싱 전략*

### REST API
HTTP 프로토콜을 사용하는 API 아키텍처 스타일. LLM 서비스는 대부분 REST API를 제공하며, POST 요청으로 프롬프트를 전송하고 JSON 응답을 받습니다.
*관련 페이지: API 기초*

### ROCm (Radeon Open Compute)
AMD GPU를 위한 오픈소스 컴퓨팅 플랫폼. CUDA의 AMD 버전이며, Ollama, LM Studio가 AMD GPU를 지원하기 위해 ROCm을 사용합니다. Linux에서만 공식 지원됩니다.
*관련 페이지: GPU 가속*

## S

### SDK (Software Development Kit)
특정 플랫폼이나 서비스를 쉽게 사용할 수 있도록 제공되는 라이브러리와 도구 모음. Claude Python SDK, OpenAI Python SDK 등이 있습니다. REST API보다 편리하며 타입 안전성을 제공합니다.
*관련 페이지: API 기초*

### Sonnet (소네트)
Claude 모델 라인업에서 성능과 비용의 균형형 티어를 가리키는 명칭입니다. 대부분의 Vibe Coding 작업에 넓게 사용됩니다.
*관련 페이지: LLM 모델 비교*

### SQLite
파일 기반 경량 관계형 데이터베이스. AI CLI 도구의 대화 히스토리, 설정 저장에 자주 사용됩니다. 서버가 필요 없어 로컬 앱에 적합합니다.
*관련 페이지: LLM 개발 환경*

### SSE (Server-Sent Events)
서버에서 클라이언트로 실시간 이벤트를 전송하는 HTTP 프로토콜. LLM 스트리밍 응답은 SSE를 사용하여 토큰을 하나씩 전송합니다. WebSocket보다 간단하며 단방향 통신에 적합합니다.
*관련 페이지: 스트리밍 가이드*

### Streaming (스트리밍)
LLM이 전체 응답을 생성한 후 반환하는 대신, 토큰을 생성하는 즉시 전송하는 방식. 사용자 경험을 개선하며, 긴 응답에서 체감 속도가 빠릅니다. Claude CLI, ChatGPT 웹 인터페이스 모두 스트리밍을 사용합니다.
*관련 페이지: 스트리밍 가이드*

### System Prompt (시스템 프롬프트)
대화 시작 시 모델의 역할과 행동 방식을 정의하는 프롬프트. "당신은 친절한 프로그래밍 어시스턴트입니다" 같은 지시를 통해 모델의 톤과 스타일을 조정합니다.
*관련 페이지: 프롬프트 기본*

## T

### TDD (Test-Driven Development, 테스트 주도 개발)
테스트를 먼저 작성하고 그것을 통과하는 코드를 구현하는 개발 방법론. AI CLI 도구에게 "TDD로 개발해줘"라고 요청하면 테스트 코드를 먼저 생성합니다.
*관련 페이지: Vibe Coding 패턴*

### Temperature (온도)
LLM 출력의 무작위성을 조절하는 파라미터(0~2). 낮은 값(0.2)은 결정적이고 일관된 출력, 높은 값(1.5)은 창의적이고 다양한 출력을 생성합니다. 코드 생성은 0.2~0.5, 창작 글쓰기는 0.8~1.2가 적합합니다.
*관련 페이지: 프롬프트 최적화*

### Token (토큰)
LLM이 처리하는 텍스트의 기본 단위. 영어는 단어의 일부(서브워드), 한국어는 음절 단위로 토큰화됩니다. "Hello, world!"는 약 4 토큰, "안녕하세요"는 약 5 토큰입니다. API 비용은 토큰 수로 청구됩니다.

```python
# tiktoken으로 GPT 계열 토큰 수 계산
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode("Hello, world! 안녕하세요.")
print(len(tokens))  # 약 11 토큰

# Claude API 응답으로 실제 사용 토큰 확인
response = client.messages.create(...)
print(response.usage)  # input_tokens, output_tokens
```
*관련 페이지: 토큰 최적화, API 기초*

### Tool Use (도구 사용)
LLM이 외부 함수, API, 데이터베이스 등을 호출하여 작업을 수행하는 기능. Function Calling, MCP가 Tool Use의 구현 방법입니다. 예: 날씨 조회, 계산기, 파일 읽기/쓰기.
*관련 페이지: Tool Use 소개, MCP 소개*

### Top-k
다음 토큰을 선택할 때 확률이 높은 상위 k개 후보만 고려하는 샘플링 방법. k=50이면 상위 50개 토큰 중에서만 선택합니다. 출력의 다양성과 품질을 균형 잡는 데 사용됩니다.
*관련 페이지: 프롬프트 최적화*

### Top-p (Nucleus Sampling)
누적 확률이 p를 초과할 때까지의 토큰들만 고려하는 샘플링 방법. p=0.9이면 상위 90% 확률을 차지하는 토큰들 중에서 선택합니다. Top-k보다 동적이며 현대 LLM의 기본 설정입니다.
*관련 페이지: 프롬프트 최적화*

### Transformer (트랜스포머)
현대 LLM의 기반이 되는 신경망 아키텍처. 2017년 "Attention is All You Need" 논문에서 제안되었으며, Self-Attention 메커니즘으로 긴 컨텍스트를 효율적으로 처리합니다. GPT, Claude, BERT 모두 Transformer 기반입니다.
*관련 페이지: LLM 기초*

### TypeScript
타입 안전성을 추가한 JavaScript 슈퍼셋. LLM API SDK는 TypeScript로 작성된 경우가 많으며, 타입 힌트가 개발 경험을 개선합니다. Claude SDK, OpenAI SDK 모두 TypeScript를 지원합니다.
*관련 페이지: API 기초*

## U

### Ubuntu (우분투)
가장 인기 있는 Linux 배포판. 서버 환경에서 LLM API 서버, Ollama, Docker를 실행할 때 널리 사용됩니다. WSL2를 통해 Windows에서도 Ubuntu를 사용할 수 있습니다.
*관련 페이지: LLM 개발 환경*

### Unix (유닉스)
1970년대 개발된 운영체제. macOS, Linux는 Unix 계열이며, 터미널 명령어(ls, cd, grep 등)를 공유합니다. AI CLI 도구는 대부분 Unix 환경에 최적화되어 있습니다.
*관련 페이지: LLM 개발 환경*

### URL (Uniform Resource Locator)
웹 리소스의 주소. LLM API 엔드포인트는 URL로 표현됩니다(예: https://api.anthropic.com/v1/messages). MCP 서버도 URL로 접근할 수 있습니다.
*관련 페이지: API 기초*

## V

### Vector Database (벡터 데이터베이스)
임베딩 벡터를 저장하고 유사도 검색을 수행하는 데이터베이스. Pinecone, Weaviate, Chroma, Qdrant 등이 있으며, RAG 시스템의 핵심 구성 요소입니다.
*관련 페이지: 벡터 DB 가이드*

### Vibe Coding (바이브 코딩)
AI CLI 도구를 사용하여 자연어로 개발 의도를 전달하면 AI가 실제 코드를 작성하는 새로운 소프트웨어 개발 방식. "바이브(vibe, 분위기)"처럼 원하는 결과의 방향을 전달하는 데 집중합니다.
*관련 페이지: Vibe Coding이란?, Vibe Coding 패턴*

### Vision (비전)
이미지를 이해하고 설명하는 AI 능력. Vision 기능이 있는 모델은 이미지의 텍스트, 객체, 장면을 분석할 수 있습니다. 스크린샷 기반 디버깅, UI 복제 등에 활용됩니다.
*관련 페이지: 멀티모달 가이드*

### VRAM (Video RAM)
GPU 메모리. 로컬 LLM을 실행할 때 모델 크기만큼의 VRAM이 필요합니다. 7B 모델은 약 8GB, 13B 모델은 약 16GB, 70B 모델은 약 80GB VRAM을 요구합니다. 양자화(Quantization)로 요구 메모리를 줄일 수 있습니다.
*관련 페이지: 하드웨어 가이드, 양자화 가이드*

### VS Code (Visual Studio Code)
Microsoft가 개발한 무료 오픈소스 코드 에디터. Continue.dev, Cline, GitHub Copilot 등 AI 확장 프로그램이 풍부하여 Vibe Coding에서 가장 인기 있는 에디터입니다.
*관련 페이지: LLM 개발 환경, Continue.dev 가이드*

## W

### WebSocket (웹소켓)
양방향 실시간 통신 프로토콜. 채팅 앱, 실시간 협업 도구에서 사용되며, 일부 LLM 서비스는 WebSocket으로 스트리밍을 제공합니다. HTTP보다 낮은 지연시간을 가집니다.
*관련 페이지: 스트리밍 가이드*

### Weights (가중치)
신경망의 학습 가능한 파라미터. LLM의 "지식"은 가중치에 저장되며, 학습 과정은 최적의 가중치를 찾는 과정입니다. 모델 파일(.gguf, .safetensors)은 가중치를 저장한 것입니다.
*관련 페이지: LLM 기초*

### Windows (윈도우)
Microsoft의 운영체제. WSL2(Windows Subsystem for Linux)를 통해 Linux 환경을 실행하여 Unix 기반 AI CLI 도구를 사용할 수 있습니다. Ollama, LM Studio는 Windows 네이티브를 지원합니다.
*관련 페이지: LLM 개발 환경*

### WSL (Windows Subsystem for Linux)
Windows에서 Linux 바이너리를 실행할 수 있게 하는 호환성 계층. WSL2는 실제 Linux 커널을 사용하여 성능이 우수하며, Docker, Ollama 등을 실행할 수 있습니다.
*관련 페이지: LLM 개발 환경*

## X

### x86
Intel과 AMD CPU 아키텍처. 대부분의 데스크톱과 서버는 x86-64(64비트 x86)를 사용합니다. Ollama는 x86-64 CPU에서 AVX2 명령어를 활용하여 추론 속도를 높입니다.
*관련 페이지: 하드웨어 가이드*

### XML (eXtensible Markup Language)
구조화된 데이터를 표현하는 마크업 언어. Claude는 프롬프트에서 XML 태그를 사용하여 섹션을 구분하는 것을 권장합니다(예: `<context>...</context>`). JSON보다 가독성이 높고 중첩 구조를 명확히 표현할 수 있습니다.
*관련 페이지: 프롬프트 고급 기법*

## Y

### YAML (YAML Ain't Markup Language)
사람이 읽기 쉬운 데이터 직렬화 형식. AI CLI 도구의 설정 파일(`.aider.conf.yml`, `config.yaml`)에 자주 사용됩니다. JSON보다 간결하며 주석을 지원합니다.
*관련 페이지: LLM 개발 환경*

### Yield (생성)
Python의 제너레이터(Generator)에서 값을 하나씩 반환하는 키워드. LLM 스트리밍 응답을 처리할 때 `yield`를 사용하여 토큰을 순차적으로 생성합니다.
*관련 페이지: 스트리밍 가이드*

## Z

### Zero-shot (제로샷 학습)
예시 없이 프롬프트만으로 새로운 작업을 수행하도록 하는 방식. "이 텍스트를 요약해줘"처럼 직접적인 지시만으로 작업합니다. Few-shot보다 덜 정확하지만 토큰 소비가 적습니다.
*관련 페이지: 프롬프트 고급 기법*

### Zsh (Z Shell)
강력한 Unix 쉘. macOS의 기본 쉘이며, Oh My Zsh 프레임워크로 테마와 플러그인을 커스터마이징할 수 있습니다. AI CLI 도구는 Bash와 Zsh 모두에서 작동합니다.
*관련 페이지: LLM 개발 환경*

---

## 핵심 정리

### 용어 카테고리 분류
- **AI 기초**: LLM, Transformer, Token, Embedding
- **프롬프팅**: Zero/Few-shot, Chain-of-Thought, RAG
- **개발 도구**: Claude CLI, Cursor, Aider, Ollama, MCP
- **인프라/설정**: API, SDK, Docker, VRAM, GPU, WSL
- **고급 기법**: Fine-tuning, Agent, Tool Use
- **안전/비용**: Hallucination, Guard

### 학습 로드맵
1. **기초 용어**: LLM, Transformer, Token, Embedding 등 AI 모델의 핵심 개념을 이해하는 것이 첫 번째 단계입니다.
2. **프롬프팅 기법**: Zero-shot, Few-shot, Chain-of-Thought, RAG 등 프롬프트 전략을 알면 AI 활용 능력이 크게 향상됩니다.
3. **개발 도구**: Claude CLI, Cursor, Aider, Ollama, MCP 등 실무에서 사용하는 도구들의 특징과 차이를 파악하세요.
4. **인프라 지식**: API, SDK, VRAM, Docker 등 개발 환경 설정에 필요한 용어를 숙지하면 시행착오를 줄일 수 있습니다.
5. **활용 팁**: 알파벳 빠른 이동 네비게이션을 사용하여 원하는 용어를 빠르게 찾고, 관련 페이지 링크로 심화 학습을 진행하세요.
