
    
    
@app.route('/static/provas/<path:filename>')
def enviar_foto(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'provas'), filename)