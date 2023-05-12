"""
ocr_text 약간의 전처리
,, -> ,
,. -> ,
., -> ,



orc_text에 적합하지 않은 값 삭제
Theimag youare requesting does not exist or is no longer available., imgur.com : 40 개


len_ocr_text <= 70 값 삭제 : 8295 개 

해시태그와 ocr 결과값 모두 없는 경우 len(ocr_text + hashtag) >= 0 삭제 : 2482 + 44 + 18 + 78 개

"""