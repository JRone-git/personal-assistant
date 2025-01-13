
def allowed_file(filename):

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class DocumentReader:

    def read_file(self, filepath):

        with open(filepath, 'r') as file:

            content = file.read()

            return {

                'title': filepath.split('/')[-1],

                'content': content,

                'type': filepath.split('.')[-1]

            }



document_reader = DocumentReader()