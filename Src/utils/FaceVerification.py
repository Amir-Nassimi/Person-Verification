import tensorflow as tf
from numpy import array as to_array
from person_verification.Src.main_algorithm.Modules.mydeepface import DeepFace

class Face_verification:

    def __init__(self, db_path, mymodel, mymetric, myfacedetector, known_regular_mean_thr, known_regular_single_thr, known_strict_mean_thr, known_strict_single_thr, unknown_mean_thr, unknown_single_thr, arg_representations, device):
        self.db_path = db_path
        self.mymodel = mymodel
        self.mymetric = mymetric
        self.myfacedetector = myfacedetector
        self.known_regular_mean_thr = known_regular_mean_thr
        self.known_regular_single_thr = known_regular_single_thr
        self.known_strict_mean_thr = known_strict_mean_thr
        self.known_strict_single_thr = known_strict_single_thr
        self.unknown_mean_thr = unknown_mean_thr
        self.unknown_single_thr = unknown_single_thr

        self.myver = DeepFace.find_config(arg_representations, device)

    def find_mean_owner(self, df):
        df = df.sort_values(by=['identity'])
        people = df['identity']
        distance = df[self.mymodel + '_' + self.mymetric].to_list()

        mydist = {}
        myrep = {}
        tmp = 'tmp'

        for idx, name in enumerate(people):
            if tmp == name:
                mydist[name] = mydist[name] + distance[idx]
                myrep[name] = myrep[name] + 1
            else:
                mydist[name] = distance[idx]
                myrep[name] = 1
                tmp = name

        for i in mydist:
            mydist[i] = mydist[i] / myrep[i]

        temp = min(mydist.values())
        return [key for key in mydist if mydist[key] == temp], min(mydist.values())

    def comparison(self, owner_mean, owner_sing, mindist_mean, mindist_sing):
        if (owner_mean == owner_sing) and (mindist_sing <= self.known_strict_single_thr) and (mindist_mean <= self.known_strict_mean_thr):
            return owner_sing, True, True

        elif (owner_mean == owner_sing) and (mindist_sing <= self.known_regular_single_thr) and (mindist_mean <= self.known_regular_mean_thr):
            return owner_sing, True, False

        elif (owner_mean != owner_sing) and (mindist_sing <= self.known_strict_single_thr) and (mindist_mean <= self.known_strict_mean_thr):
            if mindist_sing >= mindist_mean:
                return owner_mean, True, True
            else:
                return owner_sing, True, True

        elif (owner_mean != owner_sing) and (mindist_sing <= self.known_regular_single_thr) and (mindist_mean <= self.known_regular_mean_thr):
            if mindist_sing >= mindist_mean:
                return owner_mean, True, False
            else:
                return owner_sing, True, False

        elif (mindist_sing >= self.unknown_single_thr) and (mindist_mean >= self.unknown_mean_thr):
            return None, False, False

        else:
            return None, None, None

    def verify(self, img_path):
        df = self.myver.find(img_path=img_path,
                             db_path=self.db_path,
                             distance_metric=self.mymetric,
                             model_name=self.mymodel,
                             detector_backend=self.myfacedetector,
                             enforce_detection=False)[0]

        if len(df) != 0:
            owner_sing, mindist_sing = df.iloc[0]['identity'], df.iloc[0][self.mymodel + '_' + self.mymetric]
            owner_mean, mindist_mean = self.find_mean_owner(df)
            ID, known_flag, strict_flag = self.comparison(
                owner_mean[0], owner_sing, mindist_mean, mindist_sing)
            return ID, known_flag, strict_flag
        else:
            return None, None, None


class Summary:
    def __init__(self,
                 db_path,
                 mymodel,
                 mymetric,
                 myfacedetector,
                 known_regular_mean_thr,
                 known_regular_single_thr,
                 known_strict_mean_thr,
                 known_strict_single_thr,
                 unknown_mean_thr,
                 unknown_single_thr,
                 arg_representations,
                 emotion_flag,
                 emotion_actions,
                 device):

        self.fv = Face_verification(db_path=db_path,
                                    mymodel=mymodel,
                                    mymetric=mymetric,
                                    myfacedetector=myfacedetector,
                                    known_regular_mean_thr=known_regular_mean_thr,
                                    known_regular_single_thr=known_regular_single_thr,
                                    known_strict_mean_thr=known_strict_mean_thr,
                                    known_strict_single_thr=known_strict_single_thr,
                                    unknown_mean_thr=unknown_mean_thr,
                                    unknown_single_thr=unknown_single_thr,
                                    arg_representations=arg_representations,
                                    device=device)

        self.emotion_flag = emotion_flag
        self.emotion_actions = emotion_actions
        self.myfacedetector = myfacedetector

        self.actions_dic = {'age': 'age',
                            'gender': 'dominant_gender',
                            'emotion': 'dominant_emotion'}

        if device == 'gpu' and not tf.test.gpu_device_name():
            raise ValueError('The GPU has not properly configured.')

    def my_verification(self, all_results, detected_images, image_info):
        if not self.emotion_flag:
            for idx, img in enumerate(detected_images):
                ID, known_flag, strict_flag = self.fv.verify(to_array(img))
                if ID != None:
                    all_results[image_info[idx]['Frame_number']][image_info[idx]['Person_number']]['ID'] = ID
                # all_results[image_info[idx]['Frame_number']][image_info[idx]['Person_number']]['Strict_flag'] = strict_flag
            return all_results
        else:
            for idx, img in enumerate(detected_images):
                ID, known_flag, strict_flag = self.fv.verify(to_array(img))
                if ID != None:
                    all_results[image_info[idx]['Frame_number']][image_info[idx]['Person_number']]['ID'] = ID
                # all_results[image_info[idx]['Frame_number']][image_info[idx]['Person_number']]['Strict_flag'] = strict_flag

                emotion_result = DeepFace.analyze(to_array(img), actions = self.emotion_actions, enforce_detection=False, detector_backend=self.myfacedetector)
                for emotion in self.emotion_actions:
                    all_results[image_info[idx]['Frame_number']][image_info[idx]['Person_number']][emotion] = emotion_result[0][self.actions_dic[emotion]]
            return all_results