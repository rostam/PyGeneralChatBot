import fasttext as ft

intents = []
with open('intents', 'r') as f:
    for d in f.read().split("\n"):
        if d != "":
            intents.append(d)

# model = ft.train_supervised('train3.csv')
# model.save_model("tvmodel.bin")

model = ft.load_model('tvmodel.bin')
res = model.predict("schalte auf ARD", k=3)
print(res[1][0])
for i,r in enumerate(res[0]):
    index_ = int(r[r.rindex('_')+1:])
    print(index_ - 1)
    print(intents[index_ - 1], res[1][i])
