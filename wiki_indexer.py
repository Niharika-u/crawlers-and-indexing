import pyterrier as pt
import glob
import os

if not pt.started():
    pt.init()

collection_path = os.getcwd() + "/files/"
text_files = glob.glob(os.path.join(collection_path, "*.txt"))
print(text_files)

index_path = "./index1"

indexer = pt.FilesIndexer(verbose=True, index_path=index_path)
indexer.setProperty('meta.forward.keys', "filename")
indexref = indexer.index(text_files)
index = pt.IndexFactory.of(indexref)

# Fetching the documents related to term "Cork"
tfidf = pt.BatchRetrieve(index, wmodel="TF_IDF", metadata=["docno", "filename"])
result = tfidf.search('Cork', sort=True)
print(result)

# Printing the file names
for index, row in result.iterrows():
    print(row['filename'], row['docno'])
