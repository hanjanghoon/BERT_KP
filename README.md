# External Knowledge Incorporated BERT for Retrieval-based Dialogue Systems
https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002785006

BERT를 사용하여 Dialog Response selection 문제 해결

BERT는 Hugging Face BERT 사용, 데이터셋으로  Ubuntu Corpus V1 사용. 외부지식으로 ubuntu command manual description 사용

외부지식을 학습 시키는 방법으로 post-training 사용 약 1%의 성능 향상

### huggingface transformers
https://github.com/huggingface/transformers

### 우분투 manual page
https://manpages.ubuntu.com/manpages/

### Abstract
인간과 상호작용하는 대화시스템을 개발하는 것은 인공지능 분야에서 중요한 문제 중 하나이다. 이러한 문제를 해결하기 위해 대화 시스템에 외부 지식을 적용하는 연구는 꾸준히 진행되어 왔다. 하지만 외부지식을 적용하기 위해서는 구조화된 지식이 필요하며, 이 지식을 생성하려면 상당한 자원이 필요하다. 이러한 관점에서 본 연구는 검색 기반 대화 시스템에서 구조화 되지 않는 텍스트를 외부지식으로 사용하는 모델을 제안한다. 기본 모델로 사전 학습된 언어모델인 BERT를 사용하고 모델이 외부지식을 학습할 수 있는 방법으로 사후 학습을 사용한다. 이 후 사후 학습된 모델을 대화 응답 선택 태스크에 fine-tuning하여 문제를 해결한다. 기존 BERT 모델에 비해 외부지식을 학습한 모델의 성능이 우분투 코퍼스에서  기준 1.3% 향상된 결과를 보였다.


![journal](https://user-images.githubusercontent.com/32722198/99933300-fcd70f00-2d9d-11eb-8bbf-8ff0c19011c4.png)
