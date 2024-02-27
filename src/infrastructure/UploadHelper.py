class UploadHelper():
    @staticmethod
    def allowedFile(filename, validExtension=None):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in validExtension

    @staticmethod
    def makeOutputFormat( value):
        return "<html><body><div id='res' >" + value + "</div></body></html>"