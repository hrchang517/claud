#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from openpyxl import load_workbook, Workbook
from werkzeug.utils import secure_filename
from io import BytesIO

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

                # 파트너 정보 추출 (B열 2번째 행)
                partner_text = str(row2_values[1] or '').strip()
                partner_type = '-'
                if '티앤씨' in partner_text:
                    partner_type = 'TNC'
                elif '티비고' in partner_text:
                    partner_type = 'TBG'

                # 상품 정보 추출 (F열)
                prod_info = str(row1_values[5] or '').strip()

                # 처리상태 추출 (E열 1번째 라인)
                status_info = str(row1_values[4] or '').strip()
                if status_info == '-':
                    status_info = ''

                # 번호, 고객명, 전화번호가 모두 있을 때만 저장
                if display_num and cust_name and phone_num:
                    customers.append({
                        'id': display_num,      # 번호 칼럼: "#102"
                        'name': cust_name,      # 고객명 칼럼: "이선아"
                        'phone': phone_num,     # 전화번호
                        'partner': partner_type,
                        'product': prod_info,
                        'status': status_info
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

@app.route('/api/download', methods=['POST'])
def download_excel():
    try:
        data = request.json
        customers = data.get('customers', [])

        if not customers:
            return jsonify({'error': '고객 데이터가 없습니다'}), 400

        # 새 Excel 파일 생성 (업로드 형식과 동일)
        wb = Workbook()
        ws = wb.active
        ws.title = "고객데이터"

        # 고객 데이터를 3행씩 추가 (업로드 형식과 동일)
        for customer in customers:
            # 파트너를 TBG/TNC에서 원래 형식으로 변환
            partner_display = '파트너: 티비고' if customer.get('partner') == 'TBG' else '파트너: (주)티앤씨'

            # Row 1: 번호, 고객명, 상품 등
            row1_data = [
                None,  # A열: 비워둠
                customer.get('id', ''),  # B열: #번호
                f"{customer.get('id', '')} {customer.get('name', '')}",  # C열: #번호 이름
                '-',  # D열: -
                None,  # E열: (행2에서 처리상태)
                customer.get('product', ''),  # F열: 상품
                None, None,  # G, H열
                '[환경] -'  # H열: [환경]
            ]
            ws.append(row1_data)

            # Row 2: 파트너 정보, 처리상태
            row2_data = [
                None,  # A열
                partner_display,  # B열: 파트너
                None,  # C열
                None,  # D열
                customer.get('status', ''),  # E열: 처리상태
            ]
            ws.append(row2_data)

            # Row 3: 연락처
            row3_data = [
                None,  # A열
                None,  # B열
                customer.get('phone', ''),  # C열: 연락처
            ]
            ws.append(row3_data)

        # 열 너비 자동 조정
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['E'].width = 30
        ws.column_dimensions['F'].width = 35

        # 메모리에 파일 저장
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        today = datetime.now().strftime("%Y%m%d")
        filename = f'{today}_backup.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        import traceback
        print(f"❌ Excel 다운로드 오류: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'파일 생성 오류: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    print("Flask 앱 시작...")
    print(f"템플릿 폴더: {app.template_folder}")
    port = int(os.environ.get('PORT', 8080))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', debug=debug_mode, port=port, use_reloader=False)
