import requests
import json
import hashlib
import sys
import traceback
import time
import os
import random
import string

#curl -X POST --upload-file data1.json doc-movies-123456789012.us-east-1.cloudsearch.amazonaws.com/2013-01-01/documents/batch --header "Content-Type: application/json"
"""
{ "type": "add",
    "id":   "tt0484562",
    "fields": {
            "title": "The Seeker: The Dark Is Rising",
            "directors": ["Cunningham, David L."],
            "genres": ["Adventure","Drama","Fantasy","Thriller"],
            "actors": ["McShane, Ian","Eccleston, Christopher","Conroy, Frances",
                                     "Crewson, Wendy","Ludwig, Alexander","Cosmo, James",
                                     "Warner, Amelia","Hickey, John Benjamin","Piddock, Jim",
                                     "Lockhart, Emma"]
          }
}
"""
#curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-Type: application/json' -d'


def index_docs(_file):

    f = open(_file)
    rand_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

    docs_to_index = []
    continue_file_num = None
    try:
        continue_file_num  = int(open(".indexc" + rand_string).read().strip())
        
    except:
        continue_file_num = 0


    print("removing index file if one exists")
    try:
        os.remove(".indexrc" + rand_string)
    except:
        pass
        
    print("continuing from {}".format(str(continue_file_num)))

    total_indexed = continue_file_num
    for line in f:
        if continue_file_num != 0:
            for i in range(0, continue_file_num):
                continue
        
        concurrent_docs_to_index = 3000
        doc_template = {"type" : "add", "id" : str(hashlib.md5(line.encode("utf-8")).hexdigest()), "fields" : None}
        line = line.strip()
        #line = bytes(line, 'utf-8').decode('utf-8', 'replace')
        line_dic = json.loads(line)
        line_dic = {k.lower(): v for k, v in line_dic.items()}
        doc_template["fields"] = line_dic
        json_dic = doc_template
        docs_to_index.append(json_dic)
        
        if len(docs_to_index) % concurrent_docs_to_index == 0:
            print("collected {} docs, posting".format(str(len(docs_to_index))))
            num_tries = 0
            while 1:
                try:
                    r = requests.post("https://doc-scylla-qedo2exnilwadvk3vic7wxmrqy.us-west-2.cloudsearch.amazonaws.com/2013-01-01/documents/batch",
                                      data = json.dumps(docs_to_index), headers = {"Content-Type" : "application/json"})
                    print(r.text)
                    r.raise_for_status()
                    total_indexed += concurrent_docs_to_index
                    print("creating continue file")
                    print("Total indexed: {}".format(str(total_indexed)))
                    fc = open(".indexc" + rand_string, "w")
                    fc.write(str(total_indexed))
                    fc.close()
                    docs_to_index = []
                    print(total_indexed)
                    break
                except:
                    print("Handled: ")
                    traceback.print_exc()
                    num_tries += 1
                    if num_tries == 3:
                        total_indexed += concurrent_docs_to_index
                        ff = open("failed-to-index.txt", "a")
                        ff.write(json.dumps({_file : total_indexed, "num_attempted" : concurrent_docs_to_index}))
                        ff.write("\n")
                        ff.close()
                        fc = open(".indexc" + rand_string, "w")
                        fc.write(str(total_indexed))
                        fc.close()
                        docs_to_index = []
                        break
                    time.sleep(5)

    print("indexing last batch of documents num {}".format(str(len(docs_to_index))))
    while 1:
        try:
            r = requests.post("https://doc-scylla-qedo2exnilwadvk3vic7wxmrqy.us-west-2.cloudsearch.amazonaws.com/2013-01-01/documents/batch",
                              data = json.dumps(docs_to_index), headers = {"Content-Type" : "application/json"})
            print(r.text)
            r.raise_for_status()
            break
        except:
            print("Handled: ")
            traceback.print_exc()
            print("Sleeping and trying again")
            time.sleep(5)

if __name__ == "__main__":
    index_docs(sys.argv[1])
    os.remove(".indexc")
