import pickle
import time
import face_recognition
import contants as CONSTANTS
import cv2
from scipy.spatial import distance as dist


"""Facial Recognition System- Part of the project. Aashish Sinha"""


class FaceEmbedding:
    def __init__(self, face_id, face_embedding):
        self.face_embedding = face_embedding
        self.face_id = face_id
        self.name = None
        self.conversation_history={'created':int(time.time()),
                                   'last_seen':int(time.time())} #todo in future
        print("New person detected!")

    def get_embedding(self):
        return self.face_embedding
    
    def get_name(self):
        return self.name
    
    def edit_name(self, new_name):
        self.name = new_name
    
    def get_face_id(self):
        return self.face_id
    
    def record_seen(self): #todo
        self.conversation_history['last_seen']=int(time.time())

class Face:
    def __init__(self) -> None:
        self.cam_stream_url = CONSTANTS.CAM_SERVER_URL
        # self.cap = cv2.VideoCapture(self.cam_stream_url)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        #lip aspect ratio history
        self.lar_history=[]

        self.face_embedding_objects= self.load_face_embeddings()
        self.face_embedding_list=None
        self.load_face_embeddings()



    def get_current_image(self):
        ret, frame = self.cap.read()

        # cv2.imshow("Frame", frame)

        if not ret:
            print("Failed to capture frame for face recog from the live stream")
            return None
        
        # return frame[:, :, ::-1]
        return frame


        
    #Returns the number of faces on webcam
    def number_of_faces_deprecated(self):
        frame = self.get_current_image()
        # frame = face_recognition.load_image_file("two_people.jpg")
        face_locations = face_recognition.face_locations(frame)
        print(face_locations)
        return len(face_locations)
    
    #use this
    def number_of_faces(self):
        frame = self.get_current_image()
        face_landmarks_list = face_recognition.face_landmarks(frame)

        number_of_faces = len(face_landmarks_list)
        return number_of_faces
    
    def is_face(self):
        return True if self.number_of_faces()>0 else False

    #less value = mouth close = <=0.1
    def get_lar(self, top_lip, bottom_lip):

        #horizontal distance
        A = dist.euclidean(top_lip[0], top_lip[6])
        B = dist.euclidean(bottom_lip[0], bottom_lip[6])
    

        #vertical distance
        C = dist.euclidean(top_lip[9], bottom_lip[9])
    
        # compute the eye aspect ratio
        lar =  (2.0* C)/(A+B) 
    
        # return the eye aspect ratio
        return lar   #vertical/horizontal
    
    
        


    #returns embeddings of who is currently speaking
    def who_is_speaking(self):
        frame = self.get_current_image()
        face_landmarks_list = face_recognition.face_landmarks(frame)

        #btw
        number_of_faces = len(face_landmarks_list)

        #iterate through faces
        for face_landmarks in face_landmarks_list:
            # for facial_feature in face_landmarks.keys():
            # if facial_feature != "bottom_lip":
            #     continue
            # print("The {} in this face has the following points: {}".format(facial_feature, ))
            # d.line(face_landmarks[facial_feature], width=5)

            #current lip aspect ratio
            current_lar = self.get_lar(face_landmarks["top_lip"], face_landmarks["bottom_lip"])
            self.lar_history.append(current_lar)

    def load_face_embeddings(self):
        #open a pickle file
        try:
            with open('face_embeddings.pkl', 'rb') as f:
                self.face_embedding_objects = pickle.load(f)
        except FileNotFoundError:
            self.face_embedding_objects={}
    

    def save_face_embeddings(self):
        #save a dictionary to pickle file
        with open('face_embeddings.pkl', 'wb') as f:
            pickle.dump(self.face_embedding_objects, f)

    
    def match_face(self, unknown_face_encoding):
        self.face_embedding_list=[self.face_embedding_objects[face_embedding_obj].get_embedding() for face_embedding_obj in self.face_embedding_objects]

        results = face_recognition.compare_faces(self.face_embedding_list, unknown_face_encoding)

        for index, result in enumerate(results):
            if result:
                #face matched at index
                face_id=index
                return self.face_embedding_objects[face_id]
            

        
        #new face detected!
        face_id=len(self.face_embedding_list)
        new_face_embedding_obj = FaceEmbedding(face_id, unknown_face_encoding)
        self.face_embedding_objects[face_id] = new_face_embedding_obj
        self.face_embedding_list.append(unknown_face_encoding)
        
        return new_face_embedding_obj
    
    def detect_person(self):
        frame = self.get_current_image()
        #todo this line assumes there's only one face in camera
        try:
            current_face_encoding = face_recognition.face_encodings(frame)[0]
            person = self.match_face(current_face_encoding)
            return person
        except IndexError:
            #no person detected
            return None





        
    

if __name__ == "__main__":
    face = Face()
    while True:
        # print("No. of faces in front of camera ", face.number_of_faces())
        person = face.detect_person()
        if person != None:
            print(person.get_face_id())

        

