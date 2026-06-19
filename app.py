#!/usr/bin/env python3
import os
import sys
from flask import Flask, render_template, request, jsonify
from openpyxl import load_workbook
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        print("=== 파일 업로드 시작 ===")

        if 'file' not in request.files:
            print("❌ 파일 없음")
            return jsonify({'error': '파일을 선택하세요'}), 400

        file = request.files['file']
        print(f"파일명: {file.filename}")

        if file.filename == '':
            print("❌ 파일명 없음")
            return jsonify({'error': '파일을 선택하세요'}), 400

        if not file.filename.endswith(('.xlsx', '.xls')):
            print("❌ Excel 파일 아님")
            return jsonify({'error': 'Excel 파일만 업로드 가능합니다'}), 400

        # 파일 저장
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"파일 저장됨: {filepath}")

        # Excel 파일 읽기
        print("Excel 파일 읽기 시작...")
        wb = load_workbook(filepath)
        print(f"시트: {wb.sheetnames}")

        ws = wb.active
        print(f"활성 시트: {ws.title}")
        print(f"최대 행: {ws.max_row}, 최대 열: {ws.max_column}")

        customers = []
        print("파싱 로직: C열 우선 → B열 백업\n")

        # 3줄씩 처리 (고객 정보가 3줄로 구성됨)
        for i in range(1, ws.max_row, 3):
            try:
                row1_values = []
                row2_values = []
                row3_values = []

                # 행 데이터 추출
                for j in range(1, 13):
                    row1_values.append(ws.cell(i, j).value)
                    if i+1 <= ws.max_row:
                        row2_values.append(ws.cell(i+1, j).value)
                    if i+2 <= ws.max_row:
                        row3_values.append(ws.cell(i+2, j).value)

                # ======= C열 우선 파싱 =======
                # C열(1줄째 C칼럼) 데이터 추출
                # 예: "#102 이선아"
                customer_raw = str(row1_values[2] or '').strip()

                display_num = ''  # 번호 칼럼에 들어갈 값 (#102)
                cust_name = ''    # 고객명 칼럼에 들어갈 값 (이선아)

                # C열에서 "#" 문자가 있으면 분리
                if customer_raw and '#' in customer_raw:
                    # "#102 이선아" 형식을 공백으로 분리
                    parts = customer_raw.split(' ', 1)
                    display_num = parts[0].strip()  # "#102"
                    cust_name = parts[1].strip() if len(parts) > 1 else ''  # "이선아"
                    print(f"  ✓ Row{i}: C열에서 추출 → {display_num} | {cust_name}")

                # C열 파싱 실패시 B열 백업
                if not display_num:
                    id_val = str(row1_values[1] or '').strip()
                    if id_val and '#' in id_val:
                        display_num = id_val
                        print(f"  ✓ Row{i}: B열 백업 → {display_num}")

                # 전화번호 추출 (3번째 줄의 C열)
                phone_num = str(row3_values[2] or '').strip() if len(row3_values) > 2 else ''

                # 파트너 정보 추출 (E열)
                partner_text = str(row1_values[4] or '').lower()
                partner_type = '-'
                if '(주)' in partner_text or '티앤씨' in partner_text:
                    partner_type = 'TNC'
                elif '티비고' in partner_text:
                    partner_type = 'TBG'

                # 상품 정보 추출 (F열)
                prod_info = str(row1_values[5] or '').strip()

                # 번호, 고객명, 전화번호가 모두 있을 때만 저장
                if display_num and cust_name and phone_num:
                    customers.append({
                        'id': display_num,      # 번호 칼럼: "#102"
                        'name': cust_name,      # 고객명 칼럼: "이선아"
                        'phone': phone_num,     # 전화번호
                        'partner': partner_type,
                        'product': prod_info,
                        'status': ''
                    })
                    print(f"    ✅ 저장 완료 → ID:{display_num} | 이름:{cust_name} | 전화:{phone_num}")
                else:
                    # 데이터 누락 확인
                    missing = []
                    if not display_num: missing.append("번호(#)")
                    if not cust_name: missing.append("이름")
                    if not phone_num: missing.append("전화")
                    print(f"    ⚠️  Row{i}: 누락된 데이터 → {', '.join(missing)}")

            except Exception as e:
                print(f"  ⚠️ 행 {i} 처리 오류: {e}")
                continue

        print(f"\n총 {len(customers)}명 추출됨")

        if customers:
            # 파일 삭제
            try:
                os.remove(filepath)
            except:
                pass

            return jsonify({'success': True, 'count': len(customers), 'data': customers})
        else:
            return jsonify({'error': '데이터를 찾을 수 없습니다. Excel 파일을 다시 확인해주세요.'}), 400

    except Exception as e:
        import traceback
        print(f"\n❌ 오류 발생:")
        print(traceback.format_exc())
        return jsonify({'error': f'파일 처리 오류: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    print("Flask 앱 시작...")
    print(f"템플릿 폴더: {app.template_folder}")
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, port=port, use_reloader=False)
