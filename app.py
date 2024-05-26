from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, session
import os
import tempfile

app = Flask(__name__)
app.secret_key = '12345678987654321_abcdefghijklmnopqrstuvwxyz'

@app.route('/')
def index():
    # Clear the session on page load to remove the filename
    filename = session.pop('filename', None)
    return render_template('index.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'base_urls' not in request.files or 'redirect_urls' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    base_urls_file = request.files['base_urls']
    # print(base_urls_file)
    redirect_urls_file = request.files['redirect_urls']
    # print(redirect_urls_file)

    # Check for valid file extensions
    if not (base_urls_file.filename.endswith('.csv') or base_urls_file.filename.endswith('.txt')):
        flash('Base URLs file must be a CSV or TXT file')
        return redirect(url_for('index'))
    if not (redirect_urls_file.filename.endswith('.csv') or redirect_urls_file.filename.endswith('.txt')):
        flash('Redirect URLs file must be a CSV or TXT file')
        return redirect(url_for('index'))
    
    try:
        base_urls_content = base_urls_file.read().decode('utf-8').strip()
        # print(base_urls_content)
        redirect_urls_content = redirect_urls_file.read().decode('utf-8').strip()
        # print(redirect_urls_content)
        
        base_urls = base_urls_content.splitlines()
        # print(base_urls)
        redirect_urls = redirect_urls_content.splitlines()
        
        if not base_urls or not redirect_urls:
            flash('Files must not be empty and must contain at least one line of text')
            return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error reading files: {str(e)}')
        return redirect(url_for('index'))
    
    # Distribute base URLs to redirect URLs
    output = distribute_urls(base_urls, redirect_urls)
    # print(output[0])
    
    # Generate HTML content
    html_content = generate_html(output)
    
    # Save the HTML content to a temporary file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.html', dir='/tmp')
    with open(temp.name, 'w') as f:
        f.write(html_content)
    
    temp_file_name = os.path.basename(temp.name)
    
    session['filename'] = temp_file_name
    flash('File successfully processed. You can download it below.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    session.pop('filename', None)
    return send_from_directory('/tmp', filename, as_attachment=True, download_name='output.html')

def distribute_urls(base_urls, redirect_urls):
    output = []
    base_len = len(base_urls)
    redirect_len = len(redirect_urls)

    if base_len >= redirect_len:
        ratio = base_len // redirect_len
        remainder = base_len % redirect_len
        index = 0
        for redirect_url in redirect_urls:
            for _ in range(ratio):
                output.append((base_urls[index], redirect_url))
                index += 1
            if remainder > 0:
                output.append((base_urls[index], redirect_url))
                index += 1
                remainder -= 1
    else:
        ratio = redirect_len // base_len
        remainder = redirect_len % base_len
        index = 0
        for base_url in base_urls:
            for _ in range(ratio):
                output.append((base_url, redirect_urls[index]))
                index += 1
            if remainder > 0:
                output.append((base_url, redirect_urls[index]))
                index += 1
                remainder -= 1

    return output

def generate_html(url_pairs):
    cadena = ''
    for base_url, redirect_url in url_pairs:
        # print(base_url, redirect_url)
        data_part = redirect_url.split('/')[-1]
        if "c:/user" in base_url.lower():
            new_base = base_url.split(",")[1:]
            new_base = ",".join(new_base)
        else:new_base = str(base_url)
        if new_base.startswith("https://") or new_base.startswith("http://"):pass
        else:new_base = f"https://{new_base}"
        full_url = f'{new_base}{redirect_url}'
        # print(full_url)
        brck = f'<a href="{full_url}">{data_part}</a> '
        # print(brck)
        cadena += brck
        # print()
    # print(brck)
    html_template = f'''<p dir="ltr" style="text-align: left;"><b id="docs-internal-guid-1900c659-7fff-82b3-dfda-f3aaaab234c3"></b></p>
<p dir="ltr"><b id="docs-internal-guid-1900c659-7fff-82b3-dfda-f3aaaab234c3">{cadena}</b></p><br><br><p></p>'''
    return html_template

if __name__ == '__main__':
    app.run(debug=True)
