import fasttext as ft

intents = []
with open('intents', 'r') as f:
    for d in f.read().split("\n"):
        if d != "":
            intents.append(d)

# model = ft.train_supervised('train3.csv')
# model.save_model("tvmodel.bin")

model = ft.load_model('tvmodel.bin')
errors = []
with open('MustHaveUtterances2.csv','r') as f:
    for d in f.read().split("\n"):
        if d != "" and 'Utterance' not in d:
            splitted = d.split(",")
            res = model.predict(splitted[0], k=1)
            index_ = int(res[0][0][res[0][0].rindex('_') + 1:])
            predicted_intent = intents[index_ - 1]
            if predicted_intent != splitted[1]:
                errors.append(d+","+predicted_intent)
                # print(d,predicted_intent)

print("\n".join(errors))