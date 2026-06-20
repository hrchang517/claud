#!/usr/bin/env python3
import os
import json
from flask import Flask, render_template, request, jsonify, session
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

# Anthropic 클라이언트 초기화
client = Anthropic()

# KDP 규격 상수
KDP_SPECS = {
    '8.5x11': {'width_inches': 8.5, 'height_inches': 11, 'name': 'Letter (8.5" × 11")', 'print_cost': 2.5},
    '8x10': {'width_inches': 8, 'height_inches': 10, 'name': 'Square (8" × 10")', 'print_cost': 2.3},
    '6x9': {'width_inches': 6, 'height_inches': 9, 'name': 'Standard (6" × 9")', 'print_cost': 1.8},
}

POPULAR_THEMES = [
    '해양 생물 (물고기, 산호초, 해마)',
    '숲 동물 (사슴, 여우, 곰)',
    '정원 풍경 (꽃, 나비, 벌)',
    '기하학적 패턴 (만달라, 추상)',
    '공룡 (공룡들과 선사시대)',
    '재미있는 식사 (과일, 음식)',
]

# 메모리 기반 저장소 (실제로는 데이터베이스 사용)
user_books = {}

def get_user_book():
    """현재 사용자의 책 데이터 가져오기"""
    user_id = request.remote_addr  # 간단한 식별자
    if user_id not in user_books:
        user_books[user_id] = {
            'designs': [],
            'spec': '8.5x11',
            'target_pages': 20,
            'created_at': datetime.now().isoformat()
        }
    return user_books[user_id]

def save_user_book(book_data):
    """사용자의 책 데이터 저장"""
    user_id = request.remote_addr
    user_books[user_id] = book_data

@app.route('/')
def index():
    return render_template('kdp_coloring_book.html')

@app.route('/api/themes', methods=['GET'])
def get_themes():
    """인기 있는 색칠책 테마 반환"""
    return jsonify({'themes': POPULAR_THEMES})

@app.route('/api/specs', methods=['GET'])
def get_specs():
    """KDP 판형 규격 정보 반환"""
    specs_list = [
        {
            'id': key,
            'name': value['name'],
            'print_cost': value['print_cost']
        }
        for key, value in KDP_SPECS.items()
    ]
    return jsonify({'specs': specs_list})

@app.route('/api/generate-design', methods=['POST'])
def generate_design():
    """AI로 색칠 도안 생성"""
    try:
        data = request.json
        theme = data.get('theme', '').strip()

        if not theme:
            return jsonify({'error': '테마를 입력해주세요'}), 400

        if len(theme) > 200:
            return jsonify({'error': '테마는 200자 이내로 입력해주세요'}), 400

        # Claude를 이용해 SVG 색칠 도안 생성
        prompt = f"""당신은 전문 색칠책 일러스트레이터입니다. 다음 주제에 대한 색칠책용 SVG 라인아트를 생성하세요.

주제: {theme}

요구사항:
1. SVG 형식으로 작성 (시작 태그: <svg viewBox="0 0 800 1000" ...>)
2. 해상도: 300 DPI 표준 (800×1000 viewBox 사용)
3. 선의 굵기: 최소 1pt 이상
4. 흑백 라인아트만 (색칠할 영역 경계선만)
5. 안전 여백: 상하좌우 0.5인치 (약 60픽셀) 확보
6. 색칠하기 쉬운 크기의 영역들 (너무 작지 않게)
7. 균형잡힌 구성

완전한 SVG 코드만 반환하세요 (설명 없이)."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        svg_content = message.content[0].text

        # SVG 검증 (기본적인 체크)
        if not svg_content.strip().startswith('<svg'):
            return jsonify({'error': 'SVG 생성에 실패했습니다. 다시 시도해주세요'}), 500

        # SVG 정리 (불필요한 텍스트 제거)
        svg_content = svg_content.strip()
        if svg_content.startswith('```'):
            svg_content = svg_content[svg_content.find('<svg'):svg_content.rfind('</svg>')+6]

        return jsonify({
            'success': True,
            'svg': svg_content,
            'theme': theme,
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error generating design: {str(e)}")
        return jsonify({'error': f'도안 생성 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/book', methods=['GET'])
def get_book():
    """현재 책 구성 조회"""
    book = get_user_book()
    spec = KDP_SPECS[book['spec']]

    # 수익 계산
    target_pages = book['target_pages']
    designs_count = len(book['designs'])
    actual_pages = designs_count + 4  # 표지, 목차, 뒷표지 등 기본 페이지

    # 권장 판매가 계산
    if actual_pages <= 24:
        suggested_price = 7.99
    elif actual_pages <= 48:
        suggested_price = 9.99
    else:
        suggested_price = 12.99

    print_cost = spec['print_cost']
    royalty = max(0, (suggested_price * 0.6) - print_cost)

    return jsonify({
        'spec': book['spec'],
        'spec_name': spec['name'],
        'designs': book['designs'],
        'total_designs': len(book['designs']),
        'target_pages': book['target_pages'],
        'actual_pages': actual_pages,
        'suggested_price': suggested_price,
        'print_cost': print_cost,
        'royalty_per_book': round(royalty, 2),
        'created_at': book['created_at']
    })

@app.route('/api/book', methods=['POST'])
def update_book():
    """책 설정 업데이트 (판형, 목표 페이지)"""
    try:
        data = request.json
        book = get_user_book()

        if 'spec' in data and data['spec'] in KDP_SPECS:
            book['spec'] = data['spec']

        if 'target_pages' in data:
            target_pages = int(data['target_pages'])
            if 20 <= target_pages <= 500:
                book['target_pages'] = target_pages
            else:
                return jsonify({'error': '목표 페이지는 20~500 사이여야 합니다'}), 400

        save_user_book(book)
        return jsonify({'success': True, 'book': book})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book/add-design', methods=['POST'])
def add_design():
    """책에 도안 추가"""
    try:
        data = request.json
        book = get_user_book()

        design = {
            'id': len(book['designs']) + 1,
            'theme': data.get('theme', ''),
            'svg': data.get('svg', ''),
            'added_at': datetime.now().isoformat()
        }

        book['designs'].append(design)
        save_user_book(book)

        return jsonify({
            'success': True,
            'design_id': design['id'],
            'total_designs': len(book['designs'])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book/remove-design', methods=['POST'])
def remove_design():
    """책에서 도안 제거"""
    try:
        data = request.json
        design_id = data.get('design_id')

        book = get_user_book()
        book['designs'] = [d for d in book['designs'] if d['id'] != design_id]
        save_user_book(book)

        return jsonify({'success': True, 'total_designs': len(book['designs'])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/book/clear', methods=['POST'])
def clear_book():
    """책 전체 초기화"""
    user_id = request.remote_addr
    if user_id in user_books:
        del user_books[user_id]

    return jsonify({'success': True})

@app.route('/api/calculate-royalty', methods=['POST'])
def calculate_royalty():
    """수익 계산기"""
    try:
        data = request.json
        price = float(data.get('price', 9.99))
        pages = int(data.get('pages', 20))
        spec_id = data.get('spec', '8.5x11')

        if spec_id not in KDP_SPECS:
            return jsonify({'error': '잘못된 판형입니다'}), 400

        if not (4.99 <= price <= 299.99):
            return jsonify({'error': '판매가는 $4.99~$299.99 범위여야 합니다'}), 400

        if not (20 <= pages <= 500):
            return jsonify({'error': '페이지 수는 20~500 범위여야 합니다'}), 400

        print_cost = KDP_SPECS[spec_id]['print_cost']

        # 페이지 수에 따른 인쇄비 증가 (대략적)
        if pages > 100:
            print_cost += 0.02 * (pages - 100)

        # 60% 로열티
        royalty = (price * 0.6) - print_cost

        return jsonify({
            'price': price,
            'pages': pages,
            'print_cost': round(print_cost, 2),
            'royalty': round(max(0, royalty), 2),
            'profit_margin': round((max(0, royalty) / price) * 100, 1) if price > 0 else 0
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/kdp-checklist', methods=['GET'])
def kdp_checklist():
    """KDP 출판 체크리스트"""
    checklist = {
        'format': {
            'title': '파일 형식',
            'items': [
                {'task': 'PDF 형식 사용', 'required': True},
                {'task': 'PDF/X-1a 표준 준수', 'required': True},
                {'task': '흑백 모드 (Grayscale)', 'required': True},
            ]
        },
        'resolution': {
            'title': '해상도',
            'items': [
                {'task': '300 DPI 이상', 'required': True},
                {'task': '1200 DPI 권장', 'required': False},
            ]
        },
        'content': {
            'title': '콘텐츠',
            'items': [
                {'task': '20페이지 이상', 'required': True},
                {'task': '표지 포함', 'required': True},
                {'task': '목차 포함', 'required': False},
                {'task': '저작권 보호 (저작권 침해 없음)', 'required': True},
                {'task': '선 굵기 1pt 이상', 'required': True},
            ]
        },
        'metadata': {
            'title': '메타데이터',
            'items': [
                {'task': '책 제목 입력', 'required': True},
                {'task': '저자 이름 입력', 'required': True},
                {'task': '카테고리 선택', 'required': True},
                {'task': '키워드 5개 이상', 'required': True},
            ]
        }
    }
    return jsonify(checklist)

@app.route('/api/publishing-tips', methods=['GET'])
def publishing_tips():
    """출판 팁"""
    tips = {
        'themes': {
            'title': '인기 있는 테마',
            'items': [
                {'theme': '동물 시리즈', 'reason': '아동/성인 모두 인기', 'tip': '단계별 난이도 제공'},
                {'theme': '식물/정원', 'reason': '명상/이완 효과', 'tip': '복잡한 패턴이 판매 증가'},
                {'theme': '기하학/만다라', 'reason': '성인용 고가 상품', 'tip': '스트레스 해소 강조'},
                {'theme': '계절 주제', 'reason': '연중 수요 있음', 'tip': '시즈널 키워드 활용'},
            ]
        },
        'keywords': {
            'title': '효과적인 키워드 전략',
            'items': [
                '색칠책 (Coloring Book)',
                '어린이용 (Kids, Children)',
                '성인용 (Adult, Stress Relief)',
                '활동책 (Activity Book)',
                '창의력 (Creativity, Relaxation)',
            ]
        },
        'pricing': {
            'title': '가격 전략',
            'items': [
                {'pages': '20-40', 'price': '$6.99-$8.99', 'reason': '기본 가격대'},
                {'pages': '41-80', 'price': '$8.99-$10.99', 'reason': '표준 길이'},
                {'pages': '81-150', 'price': '$10.99-$14.99', 'reason': '프리미엄'},
                {'pages': '150+', 'price': '$14.99+', 'reason': '대작/시리즈'},
            ]
        },
        'qa': {
            'title': '품질 점검 팁',
            'items': [
                '선의 굵기 일관성 확인 (1pt 이상)',
                '페이지 여백 확인 (안전 여백 0.5")',
                'PDF 변환 전 최종 검토',
                '테스트 출판 (CreateSpace 이용)',
            ]
        }
    }
    return jsonify(tips)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', debug=debug_mode, port=port, use_reloader=False)
