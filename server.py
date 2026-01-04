"""
한국 공공 지원 상담 MCP 서버
FastMCP 기반으로 구현된 한국 공공 지원 상담을 위한 도구들
"""

from fastmcp import FastMCP
from typing import Literal, Optional

mcp = FastMCP("Korean Public Support Advisor")

# 분야 타입 정의
DomainType = Literal[
    "주거·월세",
    "생활 유지",
    "의료·돌봄",
    "고용·교육",
    "심리·정서",
    "문화·여가",
    "평생교육",
    "참여·활동"
]


@mcp.tool()
def orchestrate_full_response(
    user_message: str,
    skip_onboarding: bool = False
) -> dict:
    """
    한국 공공 지원 상담의 메인 진입 도구

    사용자가 상황을 설명하거나 지원을 요청할 때 가장 먼저 호출해야 하는 도구입니다.

    호출 필수:
    - 처음 상담을 시작할 때 (상황 설명, 지원 요청 등)
    - 분야가 불명확하거나 여러 분야가 섞여 있을 때
    - 위기 상황(성폭행, 가정폭력 등) 포함 모든 상황

    호출 금지:
    - 특정 분야가 명시된 경우 (rank_support_cards 사용)

    이 도구는 다음 단계를 자동으로 제공합니다:
    ① 상황 요약 → ② 분야 안내 → ③ 혜택 카드 2-3개 → ④ 행동 단계 →
    ⑤ 제도명(트리거 시) → ⑥ 확장 가능성 → ⑦ 감정 안전 메시지

    Args:
        user_message: 사용자의 상담 메시지
        skip_onboarding: 온보딩 과정 생략 여부

    Returns:
        상담 응답 전체 구조 (상황 요약, 분야 안내, 혜택 카드, 행동 단계, 감정 메시지 등)
    """
    # 실제 구현은 백엔드 로직에 따라 달라집니다
    return {
        "summary": f"'{user_message}'에 대한 상황 분석 완료",
        "domains": ["주거·월세", "생활 유지"],
        "cards": [
            {
                "title": "혜택 카드 1",
                "description": "이게 뭐냐면...",
                "why_now": "왜 지금 맞냐면...",
                "action": "지금 하실 수 있는 말...",
                "contact": "어디로...",
                "fallback": "막히면..."
            }
        ],
        "action_steps": {
            "today": "오늘 할 일",
            "tomorrow": "내일까지 할 일",
            "fallback": "막히면 대안"
        },
        "safe_message": "감정 안전 메시지",
        "followup_options": ["의료·돌봄", "심리·정서"]
    }


@mcp.tool()
def normalize_user_context(message: str) -> dict:
    """
    한국 공공 지원 관련 사용자 발화를 구조화된 상황 정보로 정리

    호출 시점:
    - orchestrate_full_response 대신 상황 분석만 먼저 필요할 때
    - 사용자가 상황 설명은 했지만 아직 지원 요청은 하지 않았을 때
    - 복잡한 상황을 단계적으로 분해하고 싶을 때

    예시:
    - "30대이고 서울에 살아요. 3년째 백수고 혼자 살아요"
    - "결혼 준비 중인데 천안 두정동에 살고 있어요"

    호출 금지:
    - 이미 orchestrate_full_response를 호출한 경우
    - 공공 지원과 무관한 일상 대화
    - 단순 인사나 확인 응답

    Args:
        message: 사용자 발화 메시지

    Returns:
        summary: 상황 요약
        keywords: 키워드 리스트
        missing_info: 부족한 정보
    """
    return {
        "summary": f"'{message}'로부터 추출한 상황 요약",
        "keywords": ["키워드1", "키워드2", "키워드3"],
        "missing_info": ["부족한 정보 1", "부족한 정보 2"]
    }


@mcp.tool()
def assess_urgency_level(context: dict) -> dict:
    """
    공공 지원 상황의 긴급도(1~3) 평가

    긴급도 기준:
    - Level 1 (매우 긴급): 퇴거, 위험, 응급, 폭력 등 즉각 대응 필요
    - Level 2 (긴급): 이번 달, 곧, 급한 등 단기 압박
    - Level 3 (보통): 일반적인 지원 탐색 상황

    호출 시점:
    - orchestrate_full_response가 자동으로 처리함
    - 개별적으로 긴급도만 판단할 때 (매우 드묾)

    대부분의 경우 단독 호출 불필요

    Args:
        context: 상황 정보 객체

    Returns:
        urgency_level: 긴급도 (1, 2, 3)
    """
    return {
        "urgency_level": 3,
        "reason": "일반적인 지원 탐색 상황"
    }


@mcp.tool()
def expose_available_domains() -> dict:
    """
    사용자 상황에서 열려 있는 지원 분야 목록 제공

    핵심 분야: 주거·월세 | 생활 유지 | 의료·돌봄 | 고용·교육 | 심리·정서
    확장 분야: 문화·여가 | 평생교육 | 참여·활동 (사용자 명시적 요청 시)

    호출 시점:
    - orchestrate_full_response가 ②단계에서 자동 포함
    - 개별적으로 분야 목록만 보여줄 때 (드묾)
    - "어떤 분야가 있어요?" 같은 분야 목록 질문

    대부분의 경우 단독 호출 불필요, orchestrate_full_response 사용 권장

    Returns:
        domains: 분야 리스트
        smart_suggestion: AI 추천 분야
    """
    return {
        "domains": [
            "주거·월세",
            "생활 유지",
            "의료·돌봄",
            "고용·교육",
            "심리·정서",
            "문화·여가",
            "평생교육",
            "참여·활동"
        ],
        "smart_suggestion": "주거·월세"
    }


@mcp.tool()
def rank_support_cards(domain: DomainType) -> dict:
    """
    특정 지원 분야의 혜택 카드 2-3개 제공

    중요: 특정 분야가 명시된 경우 바로 이 도구를 사용하세요.
    orchestrate_full_response를 거치지 않고 바로 호출 가능합니다.

    호출 시점:
    - 분야 키워드 + 필요/절실 표현: "월세 지원이 필요해요", "고정지원이 절실해요"
    - 분야 키워드 + 힘듦 표현: "주거가 너무 힘들어요", "생활비가 부족해요"
    - 분야 키워드 + 요청: "주거 지원 받고 싶어요", "의료 지원이 필요해요"
    - 명시적 선택: "주거 쪽으로 더 자세히", "의료 관련 지원이 궁금해요"
    - "더 자세히", "구체적으로", "다른 옵션은?" 같은 후속 질문 시

    호출 금지:
    - 분야가 불명확하거나 여러 개일 때 (orchestrate_full_response 사용)
    - 처음 상담 시작할 때 분야가 없을 때 (orchestrate_full_response 사용)

    Args:
        domain: 지원 분야 (주거·월세, 생활 유지, 의료·돌봄, 고용·교육, 심리·정서, 문화·여가, 평생교육, 참여·활동)

    Returns:
        각 카드의 "이게 뭐냐면", "왜 지금 맞냐면", "지금 하실 수 있는 말", "어디로", "막히면" 정보
    """
    return {
        "domain": domain,
        "cards": [
            {
                "card_number": 1,
                "title": f"{domain} 혜택 카드 1",
                "what_is_it": "이게 뭐냐면...",
                "why_now": "왜 지금 맞냐면...",
                "what_you_can_say": "지금 하실 수 있는 말...",
                "where_to_go": "어디로...",
                "if_blocked": "막히면..."
            },
            {
                "card_number": 2,
                "title": f"{domain} 혜택 카드 2",
                "what_is_it": "이게 뭐냐면...",
                "why_now": "왜 지금 맞냐면...",
                "what_you_can_say": "지금 하실 수 있는 말...",
                "where_to_go": "어디로...",
                "if_blocked": "막히면..."
            }
        ]
    }


@mcp.tool()
def generate_action_steps(selected_card: Optional[str] = None) -> dict:
    """
    선택한 지원에 대한 실행 계획 제공 (오늘/내일/막히면 3단계)

    호출 시점:
    - "구체적으로 어떻게 해요?", "방법 알려주세요" 요청
    - "오늘 바로 할 수 있는 게 뭐예요?" 질문
    - 카드 선택 후 실행 방법이 궁금할 때
    - "시작하려면 어떻게 하나요?" 같은 실행 의도

    예시:
    - "구체적으로 어떻게 시작하나요?"
    - "오늘 바로 할 수 있는 일이 뭐예요?"
    - "실행 계획을 알려주세요"
    - "당장 뭐부터 하면 돼요?"

    호출 금지:
    - 아직 카드를 선택하지 않았을 때
    - orchestrate_full_response가 이미 행동 단계를 포함한 경우
    - 단순 정보 질문 단계

    Args:
        selected_card: 선택한 카드 정보 (선택사항)

    Returns:
        today: 오늘 할 일
        tomorrow: 내일까지 할 일
        fallback: 막히면 대안
    """
    return {
        "today": [
            "오늘 할 일 1: 담당 기관에 전화하기",
            "오늘 할 일 2: 필요 서류 목록 확인하기"
        ],
        "tomorrow": [
            "내일까지 할 일 1: 서류 준비하기",
            "내일까지 할 일 2: 방문 예약하기"
        ],
        "fallback": "막히면: 복지 상담 전화 129로 연락하세요"
    }


@mcp.tool()
def generate_fallback_paths(issue_type: Optional[str] = None) -> dict:
    """
    전화 연결 실패, 서류 부족, 자격 애매할 때의 대안 경로 제시

    호출 시점:
    - "전화가 안 돼요", "연결이 안 되는데요" 호소
    - "서류가 없어요", "준비가 어려워요" 어려움 표현
    - "자격이 안 될 것 같은데", "조건이 애매한데" 걱정
    - 실행 중 실제 문제 발생했을 때

    예시:
    - "전화 연결이 안 되는데 어떻게 해요?"
    - "서류 준비가 너무 어려워요"
    - "자격이 애매한데 다른 방법은?"
    - "담당자가 안 받는데요"

    호출 금지:
    - 아직 시도하지 않았을 때
    - 문제 상황이 실제로 발생하지 않았을 때
    - 단순 걱정이나 예상 (실제 막힘 발생 후 호출)

    Args:
        issue_type: 문제 유형 (선택사항)

    Returns:
        전화/서류/자격 각 상황별 구체적인 대안 경로
    """
    return {
        "phone_issues": {
            "alternatives": [
                "복지로(www.bokjiro.go.kr) 온라인 신청",
                "129 콜센터 상담",
                "주민센터 방문"
            ]
        },
        "document_issues": {
            "alternatives": [
                "주민센터에서 발급 가능한 서류 목록 확인",
                "온라인 발급 서비스 활용",
                "서류 간소화 신청 가능 여부 문의"
            ]
        },
        "eligibility_issues": {
            "alternatives": [
                "복지 상담사와 1:1 상담",
                "유사한 다른 제도 탐색",
                "조건 완화된 지역별 제도 확인"
            ]
        }
    }


@mcp.tool()
def compose_safe_response(user_emotion: Optional[str] = None) -> dict:
    """
    응답 마지막에 붙는 감정 안전 메시지 생성

    호출 시점:
    - orchestrate_full_response가 ⑦단계에서 자동으로 포함함
    - 개별적으로 감정 지원 메시지만 필요할 때 (매우 드묾)
    - 사용자가 불안이나 압박을 표현했을 때

    예시 (드묾):
    - "무서워요"
    - "너무 불안해요"
    - "걱정돼요"

    대부분의 경우:
    - 단독 호출 불필요
    - orchestrate_full_response가 자동으로 처리
    - 일반적인 상담에서는 호출 금지

    Args:
        user_emotion: 사용자의 감정 상태 (선택사항)

    Returns:
        상황에 맞는 감정 안전 메시지 (비판단적, 지지적 톤)
    """
    return {
        "safe_message": "지금 이 순간 힘드신 게 당연합니다. 천천히 한 걸음씩 나아가시면 됩니다.",
        "tone": "비판단적, 지지적",
        "support_resources": [
            "복지 상담 전화 129",
            "자살 예방 상담 전화 1393",
            "정신건강 위기 상담 1577-0199"
        ]
    }


@mcp.tool()
def collect_region_context(user_input: str) -> dict:
    """
    한국 지역(시/도/군/구) 정보를 수집하여 지역별 지원 안내에 활용

    호출 시점:
    - 사용자가 지역 정보를 명시적으로 제공했을 때
    - 지역별 지원 차이를 확인해야 할 때
    - "OO에 살아요", "OO 거주" 같은 지역 언급

    예시:
    - "서울 강남구에 살아요"
    - "천안 두정동이에요"
    - "부산 사상구입니다"
    - "경기도 수원시 거주 중이에요"

    호출 금지:
    - 사용자가 지역 정보를 언급하지 않았을 때
    - 이미 지역 정보가 수집되었을 때 (중복 방지)
    - 지역과 무관한 일반 질문

    Args:
        user_input: 지역 정보가 포함된 사용자 입력

    Returns:
        collected: 수집 성공 여부
        region: 지역명
        message: 안내 메시지
    """
    return {
        "collected": True,
        "region": {
            "province": "서울특별시",
            "city": "강남구",
            "district": "역삼동"
        },
        "message": "서울 강남구 지역 정보가 수집되었습니다. 해당 지역의 특화 지원 프로그램을 안내해드릴 수 있습니다."
    }


@mcp.tool()
def reveal_policy_name_if_triggered(message: str) -> dict:
    """
    사용자가 특정 혜택 카드의 정확한 제도명을 물어볼 때 제도명 공개

    호출 시점:
    - 카드 선택 신호: "1번이 뭐예요?", "첫 번째 할게요", "2번 선택할게요"
    - 제도명 직접 질문: "정확한 이름이 뭐예요?", "제도명 알려주세요", "무슨 제도예요?"
    - 행동 의도 표현: "어디로 전화해야 해요?", "신청 방법은?", "연락처 알려주세요"

    예시:
    - "1번이 정확히 뭐예요?"
    - "첫 번째 거 선택할게요"
    - "이거 정확한 제도 이름 알려주세요"
    - "어떻게 신청하나요?"
    - "어디로 전화하면 돼요?"

    호출 금지:
    - 아직 혜택 카드를 제시하지 않았을 때
    - 일반적인 지원 정보 질문 (orchestrate_full_response 사용)
    - 분야 선택 단계

    Args:
        message: 사용자 메시지

    Returns:
        triggered: 트리거 감지 여부
        policy_name: 제도명
        message: 안내 메시지
    """
    return {
        "triggered": True,
        "policy_name": "청년 월세 한시 특별지원",
        "contact": "02-1234-5678",
        "website": "https://www.bokjiro.go.kr",
        "message": "선택하신 제도는 '청년 월세 한시 특별지원'입니다. 02-1234-5678로 문의하시거나 복지로 웹사이트에서 신청 가능합니다."
    }


@mcp.tool()
def suggest_followup_options(current_domain: Optional[str] = None) -> dict:
    """
    현재 선택한 지원 외에 추가로 살펴볼 수 있는 지원 분야 제안

    호출 시점:
    - "또 뭐가 있어요?", "다른 지원도 궁금해요" 질문
    - 한 가지 지원을 마무리하고 확장하려 할 때
    - "다른 건 없어요?", "추가로 받을 수 있는 거" 같은 추가 탐색 의도

    예시:
    - "또 받을 수 있는 지원이 있나요?"
    - "다른 것도 궁금해요"
    - "주거 말고 다른 분야는 뭐가 있어요?"
    - "추가로 알아볼 만한 게 있을까요?"

    호출 금지:
    - 첫 상담 시작 단계 (orchestrate_full_response 사용)
    - orchestrate_full_response가 이미 ⑥확장 안내를 포함한 경우
    - 아직 하나도 선택하지 않았을 때

    Args:
        current_domain: 현재 선택한 분야 (선택사항)

    Returns:
        followup_domains: 추가 분야 리스트
        message: 안내 메시지
    """
    return {
        "followup_domains": [
            {
                "domain": "의료·돌봄",
                "reason": "건강 관련 지원이 필요할 수 있습니다"
            },
            {
                "domain": "심리·정서",
                "reason": "정서적 지원도 함께 받으실 수 있습니다"
            },
            {
                "domain": "고용·교육",
                "reason": "장기적인 자립을 위한 교육 기회도 있습니다"
            }
        ],
        "message": "현재 선택하신 지원 외에도 추가로 받으실 수 있는 지원이 있습니다."
    }


if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run()
