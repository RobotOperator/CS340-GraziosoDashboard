#Created by Lance Cain 09/25/2022
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId
from urllib import parse
from bson import json_util

class AnimalShelter(object):
    #CRUD operations for Animal collection in AAC mongodb

    def __init__(self, username, password, port, db, collection):
        #Initialize the MongoClient to access mongodb collections
        #Escape the provided password in the event it contains any special characters
        self.client = MongoClient('mongodb://%s:%s@localhost:%s' % (username, parse.quote_plus(password), port))
        #Set the database
        self.database = self.client[db]
        #Set the collection
        self.collection = self.database[collection]

    #Create method implementation for CRUD
    def create(self, data=None):
        if data is not None:
            try:
                self.database.animals.insert(data) #data should be formatted as a dictionary
                return "True"
            except Exception as e:
                print(e) #print the exception and return "False" for insert failure
                return "False"
        else:
            print("Error: Nothing to save, because data parameter is empty") #Modified from raise exception to allow execution flow to contiue to return False.
            return "False"

    #Read method implementation for CRUD
    def read(self, filter=None):
        try:
            if filter is None:
                output = self.collection.find()
            else:
                output = self.collection.find(filter) #filter should be formatted as a dictionary
            return output
        except OperationFailure as e:  #return the document presented by the database on operation failure
            return e.details
        except Exception as e:   #If an error occurs that falls outside of operation failures handled by the MongoDB server return it
            return e

    #Delete many method implementation for CRUD
    def delete(self, filter=None):
        try:
            if filter is None:
                error_line = "Error: To delete all documents in the database use the preset filter 'all documents', otherwise an explicit filter must be provided as a dictionary. {'Show':'example'}"
                print(error_line)
                return error_line
            elif filter is 'all documents':
                output = self.collection.delete_many({}) #Require an explicitly passed unique parameter to delete all documents from a collection
            else:
                output = self.collection.delete_many(filter) #filter should be formatted as a dictionary
            return json_util.dumps(output.raw_result,default=json_util.default) #return the result of the delete in JSON format
        except OperationFailure as e:  #return the document presented by the database on operation failure
            return e.details
        except Exception as e:   #If an error occurs that falls outside of operation failures handled by the MongoDB server return it
            return e

    #Update many method implementation for CRUD
    def update(self, query=None, new_values=None):
        try:
            if filter is None or new_values is None:
                error_line = "Error: A filter dictionary for documents to be modified and new values to be set in those documents are required."
                print(error_line)
                return(error_line)
            else:
                output = self.collection.update_many(query,{"$set": new_values}) #query and new values should be formatted as dictionaries
            return json_util.dumps(output.raw_result,default=json_util.default) #return the result of the update in JSON format
        except OperationFailure as e:  #return the document presented by the database on operation failure
            return e.details
        except Exception as e:   #If an error occurs that falls outside of operation failures handled by the MongoDB server return it
            return e
