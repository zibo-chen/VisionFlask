from Cocoa import NSURL
from Quartz import CIImage
from Vision import VNImageRequestHandler, VNRecognizeTextRequest


class TextRecognizer:
    def __init__(self, recognition_languages=["zh-Hans", "en"]):
        self.recognition_languages = recognition_languages
        self.results = []

    def handle_request(self, request, error):
        if error:
            print(f"Error: {error}")
            return
        observations = request.results()
        for observation in observations:
            top_candidate = observation.topCandidates_(1)[0]
            bounding_box = observation.boundingBox()
            # Convert bounding box to list [x, y, width, height]
            bbox_list = [bounding_box.origin.x, bounding_box.origin.y, bounding_box.size.width,
                         bounding_box.size.height]
            self.results.append((top_candidate.string(), bbox_list))

    def recognize_text_from_image(self, image_path):
        self.results = []
        image_url = NSURL.fileURLWithPath_(image_path)
        ci_image = CIImage.alloc().initWithContentsOfURL_(image_url)

        request = VNRecognizeTextRequest.alloc().initWithCompletionHandler_(self.handle_request)
        request.setRecognitionLanguages_(self.recognition_languages)

        handler = VNImageRequestHandler.alloc().initWithCIImage_options_(ci_image, None)
        success, error = handler.performRequests_error_([request], None)

        if not success:
            print(f"Failed to perform text recognition: {error}")
            return []

        return self.results
