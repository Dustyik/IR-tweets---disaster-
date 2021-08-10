import pandas as pd
import torchtext
import torch
import random
from torchtext.data.utils import get_tokenizer
from collections import Counter
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch import nn
from gensim.models import KeyedVectors
import gensim.downloader as api

class Ranking_model(nn.Module):
    def __init__(self, vocab):
        super(Ranking_model, self).__init__()

        #embedding matix, convert tokens to vectors
        self.embedding = nn.Embedding(num_embeddings=len(vocab), 
                                    embedding_dim=50, 
                                    padding_idx=vocab.stoi['<pad>'])

        #Exercise:1
        #define the LSTM encoder here.
        self.encoder = nn.LSTM(50, 50, batch_first=True)

        #feedforward layer
        self.nn_layer1 = nn.Linear(in_features=50*2, out_features=1)


    def forward(self, qry_tokens, pos_doc_tokens, neg_doc_tokens):

        qry_embedded = self.embedding(qry_tokens)
        pos_doc_embedded = self.embedding(pos_doc_tokens)
        neg_doc_embedded = self.embedding(neg_doc_tokens)


        #Exercise:2
        #pass the query, positive, and negative document through the encoder
        out_qry = torch.mean(self.encoder(qry_embedded)[0],1)
        out_pos = torch.mean(self.encoder(pos_doc_embedded)[0],1)
        out_neg = torch.mean(self.encoder(neg_doc_embedded)[0],1)

        #Exercise:3
        #concat query-positive document and query-negative document
        concat_q_pos_doc = torch.cat((out_qry, out_pos),1)
        concat_q_neg_doc = torch.cat((out_qry, out_neg),1)


        #Exercise:4
        #feedforward layer inplace of question marks
        pos_score = torch.relu(self.nn_layer1(concat_q_pos_doc))
        neg_score = torch.relu(self.nn_layer1(concat_q_neg_doc))

        diff = pos_score - neg_score

        return diff

class PairwiseLTR:

    def __init__(self, tweets_data, titles_data, max_doc_len=50, max_query_len=50, batch_size=128, method="trim"):
        self.data = tweets_data
        self.data = self.data.replace({"relevance_score":2}, 1)
        self.titles = titles_data
        self.articles_id = list(self.data.article_id.unique())
        self.get_pos_neg(method)
        self.init_model_parameters(max_doc_len, max_query_len) #cretes a train_test_split for the article titles
        self.batch_size = batch_size
        self.train_dataloader = DataLoader(self.train_dataset, batch_size=self.batch_size,
                                    shuffle=True, collate_fn=self.collate_batch)
        self.valid_dataloader = DataLoader(self.valid_dataset, batch_size=self.batch_size,
                                    shuffle=False, collate_fn=self.collate_batch)
        try:
            #load model
            self.model = torch.load("PairwiseLTRModel.pt")
            self.model.eval()
        except:
            self.model = Ranking_model(self.vocab)
            self.model.to(self.device)
            self.init_glove()
            self.train()
            
    def return_test_articles(self):
        return self.test_articles

    def get_pos_neg(self, method):
        self.pos_ = {}
        self.neg_ = {}
        self.articles_id = list(self.data.article_id.unique())
        to_remove = []
        for i in self.articles_id:
            temp = self.data[self.data["article_id"]==i]
            temp["relevance_score"].sum()
            num_pos = temp["relevance_score"].sum()
            num_neg = temp.shape[0] - num_pos
            if method=="trim":
                num_keep = min(num_pos, num_neg)
                pos_list = list(temp[temp["relevance_score"]==1].clean_text[:num_keep])
                neg_list = list(temp[temp["relevance_score"]==0].clean_text[:num_keep])
            elif method=="pad":
                pos_list = list(temp[temp["relevance_score"]==1].clean_text)
                neg_list = list(temp[temp["relevance_score"]==0].clean_text)
                if num_pos==0 or num_neg==0:
                    to_remove.append(i)
                    continue
                if num_pos<num_neg:
                    for j in range(num_neg-num_pos):
                        pos_list.append(pos_list[-1])
                elif num_neg<num_pos:
                    for j in range(num_pos-num_neg):
                        neg_list.append(neg_list[-1])
            self.pos_[i] = pos_list
            self.neg_[i] = neg_list
        for i in to_remove:
            self.articles_id.remove(i)
    
    def init_model_parameters(self, max_doc_len, max_query_len):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer = get_tokenizer("basic_english")
        self.train_articles, self.test_articles = train_test_split(self.articles_id, test_size=1.5/10, random_state=179)
        dataset = []
        for i in self.train_articles:
            for j in range(len(self.pos_[i])):
                dataset.append([self.titles[self.titles["id"]==i].title.to_list()[0], self.pos_[i][j], self.neg_[i][j]])
        self.train_dataset, self.valid_dataset = train_test_split(dataset, test_size=1/9, random_state=179)
        self.counter = Counter()
        for (qry, pos, neg) in self.train_dataset:
            self.counter.update(self.tokenizer(pos))
            self.counter.update(self.tokenizer(neg))
        self.vocab = torchtext.vocab.Vocab(self.counter, max_size=10000,  specials=('<pad>', '<unk>'), specials_first=True)
        
        #tokenization function
        self.text_pipeline = lambda x: [self.vocab[token] for token in self.tokenizer(x)]

        #padding function
        self.query_padding_pipeline = lambda tokens: [self.vocab.stoi['<pad>'] for p in range(max_query_len - len(tokens))] + tokens[-max_query_len:]
        self.doc_padding_pipeline = lambda tokens: [self.vocab.stoi['<pad>'] for p in range(max_doc_len - len(tokens))] + tokens[:max_doc_len]
        
    def collate_batch(self, batch):

        #initizlize empty lists for query and doc lists
        query_list, pos_doc_list, neg_doc_list = [], [], []

        for (qry, pos, neg) in batch:


            #query -> tokens -> id -> pad to max query length
            qry_ = self.query_padding_pipeline(self.text_pipeline(qry))

            #doc -> tokens -> ids -> pad to max doc length
            pos_ = self.doc_padding_pipeline(self.text_pipeline(pos))
            
            neg_ = self.doc_padding_pipeline(self.text_pipeline(neg))

            query_list += [qry_]
            pos_doc_list += [pos_]
            neg_doc_list += [neg_]

        #shuffle samples
        temp = list(zip(query_list, pos_doc_list, neg_doc_list))
        random.shuffle(temp)
        query_list, pos_doc_list, neg_doc_list = zip(*temp)

        #Now we have numbers, load them to tensors and put on GPU
        query_list = torch.tensor(query_list, dtype=torch.int64)

        pos_doc_list = torch.tensor(pos_doc_list, dtype=torch.int64)
        neg_doc_list = torch.tensor(neg_doc_list, dtype=torch.int64)
        return query_list.to(self.device), pos_doc_list.to(self.device), neg_doc_list.to(self.device)

    def init_glove(self):
        try:
            print("Loading saved word vectors...")
            glove_50dim = KeyedVectors.load("./glove_50dim.w2v")
        except:
            print("Downloading word vectors...")
            glove_50dim = api.load("glove-wiki-gigaword-50")
            glove_50dim.save('glove_50dim.w2v')

        print("Number of word vectors:", glove_50dim.vectors.shape)

        #Initialise model embedding with glove
        for word in self.vocab.stoi.keys():
            if word in glove_50dim.key_to_index.keys():
                word_vec = glove_50dim[word]
                self.model.embedding.weight.data[self.vocab.stoi[word]] = torch.tensor(word_vec)\

    def train(self, num_epochs=10):
        optimizer=torch.optim.AdamW(self.model.parameters(), lr=1e-5)
        for epoch in range(num_epochs):
            print("-->Epoch:{}".format(epoch))

            epoch_train_loss = 0.0
            self.model.train()
            for idx, (qry_tokens, pos_doc_tokens, neg_doc_tokens) in enumerate(self.train_dataloader):
                #flush the gradient values
                optimizer.zero_grad()
                #calculate model output
                diff = self.model(qry_tokens, pos_doc_tokens, neg_doc_tokens)

                #Exercise:5.1
                #write pairwise loss here
                loss = torch.log(1 + torch.exp(-1*diff)).mean()

                #backward pass
                loss.backward() 

                #weights update
                optimizer.step()

                #average train loss
                epoch_train_loss += loss.cpu().item()*self.batch_size

                print("Batch {}/{}, avg. train loss is {}".format(idx, len(self.train_dataloader), epoch_train_loss/(idx+1)), end='\r')


            #validation
            epoch_val_loss = 0.0
            self.model.eval()
            with torch.no_grad(): #weights should not update
                for idx, (qry_tokens, pos_doc_tokens, neg_doc_tokens) in enumerate(self.valid_dataloader):
                    #formward pass
                    diff = self.model(qry_tokens, pos_doc_tokens, neg_doc_tokens) 

                    #Exercise:5.2
                    epoch_val_loss += torch.log(1 + torch.exp(-1*diff)).mean() #same loss as in training

                print("\nval loss:{}".format(epoch_val_loss))
        torch.save(self.model, "PairwiseLTRModel.pt")
                
    def rank_docs(self, qry):
        doc_list = self.data.tweet.tolist()
        scores = []
        for doc in doc_list:
            self.model.eval()
            with torch.no_grad():
                qry_ = torch.tensor([self.query_padding_pipeline(self.text_pipeline(qry))], dtype=torch.int64).to(self.device)
                doc_ = torch.tensor([self.doc_padding_pipeline(self.text_pipeline(doc))], dtype=torch.int64).to(self.device)
                score = self.model(qry_, doc_, doc_*0)
                scores.append((doc, score.detach().item()))
                # print("query [{}] to doc [{}] matching score [{}]\n".format(qry, doc, score.detach().item()))
        scores = sorted(scores, key = lambda x: x[1])
        results = pd.DataFrame(columns=['article_id', 'tweet_id', 'relevance_score', 'tweet', 'clean_text'])
        for doc, score in scores:
            doc_filt = self.data[self.data["tweet"]==doc]
            if doc not in results["tweet"].to_list():
                try:
                    results = results.append(doc_filt.iloc[0])
                except:
                    pass
        return results
    

# max_doc_len = 50
# max_qry_len = 50
# batch_size = 128
# method = "trim"
# # test = [(50, 50, 128, "pad"),(50, 50, 256, "pad"),(75, 75, 128, "pad"),(75, 75, 256, "pad")]
# test = [(50, 50, 128, "trim"),(50, 50, 256, "trim"),(25, 25, 128, "trim"),(25, 25, 256, "trim")]
# avg = []
# for i in test:
#     print(i)
#     t = PairwiseLTR(i[0], i[1], i[2], i[3])
#     t.train()
#     rank_scores = []
#     for i in t.test_articles:
#         data_ = t.data[t.data["article_id"]==i].sort_values(by='relevance_score', ascending=False)
#         qry = t.titles[t.titles["id"]==i].title.to_list()[0]
#         tweets = t.data[t.data["article_id"]==i].tweet.to_list()
#         scores = t.rank_docs(qry, tweets)
#         # tweet_score = sorted(list(zip(tweets, scores)), key = lambda x: x[1])
#         rel_tweets = data_[data_["relevance_score"]==1].tweet.to_list()
#         rank_score = 0
#         for i in scores[:len(rel_tweets)]:
#             if i[0] in rel_tweets:
#                 rank_score += 1
#         if len(rel_tweets)>9:
#             rank_scores.append(rank_score/len(rel_tweets))
#         print(f"{rank_score}/{len(rel_tweets)}")
#     print(average(rank_scores))
#     avg.append(average(rank_scores))

# print(avg)
# for i in zip(test, avg):
#     print(f"doc length: {i[0][0]}, qry length: {i[0][1]}, batch size: {i[0][2]}, method: {i[0][3]} \naverage score: {i[1]}")

#t = PairwiseLTR(50, 50, 128, "trim")
# t.train()
# rank_scores = []
#for i in t.test_articles:
#    print(i)
    # data_ = t.data[t.data["article_id"]==i].sort_values(by='relevance_score', ascending=False)
    # qry = t.titles[t.titles["id"]==i].title.to_list()[0]
    # tweets = t.data[t.data["article_id"]==i].tweet.to_list()
    # scores = t.rank_docs(qry, tweets)
    # print(scores)