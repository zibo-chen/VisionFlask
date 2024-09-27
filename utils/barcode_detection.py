from Cocoa import NSURL
from Quartz import CIImage
from Vision import VNImageRequestHandler, VNDetectBarcodesRequest


class BarcodeDetector:
    def __init__(self):
        self.results = []

    def handle_request(self, request, error):
        if error:
            print(f"Error: {error}")
            return
        observations = request.results()
        for observation in observations:
            bounding_box = observation.boundingBox()
            # Convert bounding box to list [x, y, width, height]
            bbox_list = [bounding_box.origin.x, bounding_box.origin.y, bounding_box.size.width,
                         bounding_box.size.height]
            barcode_value = observation.payloadStringValue()
            symbology = observation.symbology()
            self.results.append((barcode_value, symbology, bbox_list))

    def detect_barcodes_from_image(self, image_path):
        self.results = []
        image_url = NSURL.fileURLWithPath_(image_path)
        ci_image = CIImage.alloc().initWithContentsOfURL_(image_url)

        request = VNDetectBarcodesRequest.alloc().initWithCompletionHandler_(self.handle_request)

        handler = VNImageRequestHandler.alloc().initWithCIImage_options_(ci_image, None)
        success, error = handler.performRequests_error_([request], None)

        if not success:
            print(f"Failed to perform barcode detection: {error}")
            return []

        return self.results


if __name__ == '__main__':
    detector = BarcodeDetector()
    results = detector.detect_barcodes_from_image("/Users/chenzibo/Downloads/Camera Roll/WIN_20240926_21_50_54_Pro.jpg")

    for barcode_value, symbology, bbox in results:
        print(f"Detected barcode: {barcode_value}")
        print(f"Symbology: {symbology}")
        print(f"Bounding box: {bbox}")
        print("---")
