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
        print("파싱 로직: B열 #숫자 기준\n")

        # B열의 #숫자 기준으로 고객 정보 추출
        i = 1
        while i <= ws.max_row:
            try:
                b_val = ws.cell(i, 2).value

                # B열에 #숫자가 있으면 새로운 고객 레코드 시작
                if b_val and isinstance(b_val, str) and b_val.startswith('#'):
                    display_num = b_val  # 번호: B열의 #숫자
                    cust_name = ''
                    phone_num = ''
                    partner_type = '-'
                    prod_info = ''
                    status_info = ''

                    # B열이 바뀔 때까지 같은 고객 정보 수집
                    j = i
                    rows_data = []

                    while j <= ws.max_row:
                        b_next = ws.cell(j, 2).value
                        # B열이 바뀌면 루프 종료
                        if j > i and b_next and isinstance(b_next, str) and b_next.startswith('#'):
                            break

                        # 각 행의 데이터 수집
                        c_val = str(ws.cell(j, 3).value or '').strip()
                        e_val = str(ws.cell(j, 5).value or '').strip()
                        g_val = str(ws.cell(j, 7).value or '').strip()
                        h_val = str(ws.cell(j, 8).value or '').strip()
                        b_val_current = str(b_next or '').strip()

                        rows_data.append({
                            'row': j,
                            'b': b_val_current,
                            'c': c_val,
                            'e': e_val,
                            'g': g_val,
                            'h': h_val
                        })
                        j += 1

                    # 수집된 행들에서 필요한 정보 추출
                    for idx, row_info in enumerate(rows_data):
                        # 이름 추출 (C열 형식: "#이름 → #번호" 또는 "#번호 이름 → #번호")
                        if not cust_name and row_info['c'] and '#' in row_info['c']:
                            if '→' in row_info['c']:
                                # "→" 기준으로 분리 후 왼쪽 부분에서 이름 추출
                                left_part = row_info['c'].split('→')[0].lstrip('#').strip()
                                if ' ' in left_part:
                                    # "#번호 이름" 형식: 공백 뒤의 이름 추출
                                    cust_name = left_part.split(' ', 1)[1]
                                else:
                                    # "#이름" 형식: 그대로 사용
                                    cust_name = left_part
                            else:
                                # 기존 형식: 공백으로 분리
                                parts = row_info['c'].split(' ', 1)
                                if len(parts) > 1:
                                    cust_name = parts[1]

                        # 전화번호 추출 (C열에서 010-로 시작)
                        if not phone_num and row_info['c'].startswith('010-'):
                            phone_num = row_info['c']

                        # 파트너 정보 추출 (B열 값이 있을 때)
                        if partner_type == '-' and row_info['b']:
                            if '티앤씨' in row_info['b']:
                                partner_type = 'TNC'
                            elif '티비고' in row_info['b']:
                                partner_type = 'TBG'

                        # 상품 정보 추출 (H열 첫 번째 행만)
                        if not prod_info and idx == 0 and row_info['h']:
                            prod_info = row_info['h']

                    # 처리상태 추출 (G열 1행 + G열 3행)
                    g1_status = ''
                    g3_status = ''
                    for idx, row_info in enumerate(rows_data):
                        if idx == 0 and row_info['g']:
                            g1_status = row_info['g']
                        if idx == 2 and row_info['g']:
                            g3_status = row_info['g']

                    # G열 1행과 3행 조합
                    status_combined = []
                    if g1_status and g1_status != '-':
                        status_combined.append(g1_status)
                    if g3_status and g3_status != '-':
                        status_combined.append(g3_status)
                    status_info = ', '.join(status_combined) if status_combined else ''

                    # 번호, 고객명, 전화번호가 모두 있을 때만 저장
                    if display_num and cust_name and phone_num:
                        customers.append({
                            'id': display_num,
                            'name': cust_name,
                            'phone': phone_num,
                            'partner': partner_type,
                            'product': prod_info,
                            'status': status_info
                        })
                        print(f"  ✅ {display_num} | {cust_name} | {phone_num} | {partner_type}")
                    else:
                        missing = []
                        if not display_num: missing.append("번호")
                        if not cust_name: missing.append("이름")
                        if not phone_num: missing.append("전화")
                        print(f"  ⚠️  {display_num}: 누락 → {', '.join(missing)}")

                    i = j  # 다음 B열 #숫자로 이동
                else:
                    i += 1

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

        # 고객 데이터를 4행씩 추가 (업로드 형식과 동일)
        for customer in customers:
            # 파트너를 TBG/TNC에서 원래 형식으로 변환
            partner_display = '파트너: 티비고' if customer.get('partner') == 'TBG' else '파트너: (주)티앤씨'

            # Row 1: 번호, 고객명, 상품
            row1_data = [
                None,  # A열
                customer.get('id', ''),  # B열: #번호
                f"{customer.get('id', '')} {customer.get('name', '')}",  # C열: #번호 이름
                '-',  # D열: -
                None,  # E열
                None,  # F열
                None,  # G열
                customer.get('product', ''),  # H열: 상품
            ]
            ws.append(row1_data)

            # Row 2: 파트너 정보, 처리상태
            row2_data = [
                None,  # A열
                partner_display,  # B열: 파트너
                None,  # C열
                None,  # D열
                None,  # E열
                None,  # F열
                customer.get('status', ''),  # G열: 처리상태
            ]
            ws.append(row2_data)

            # Row 3: 연락처
            row3_data = [
                None,  # A열
                None,  # B열
                customer.get('phone', ''),  # C열: 연락처
            ]
            ws.append(row3_data)

            # Row 4: E(진행상태) | G(처리상태)
            row4_data = [
                None,  # A열
                None,  # B열
                None,  # C열
                None,  # D열
                customer.get('row4_e', ''),  # E열: 진행상태
                None,  # F열
                customer.get('row4_g', ''),  # G열: 처리상태
            ]
            ws.append(row4_data)

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
