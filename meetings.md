# Meetings notes

## Meeting 1.
* DATE: 11.2.2021 14:20-14:40
* ASSISTANTS: Mika Oja

### Minutes
Summary of what was discussed during the meeting

The aim of the project, Image Annotator (IA) Web API, was briefly introduced and presented with wiki documentation of the project. We briefly discussed the content of the aimed IA Web API, the objectives of the PWP course, and the objectives of the documentation in the wiki. For the most part, text of wiki project documentation was acceptable, but it needed some refining, additions, and transfers to meet the aimed specifications.

We discussed the project description in 'Overview', and why the IA Web API will be useful in the future, and what type of use cases are planned for the API to be implemented within the course. Chapter 'Overview 'did not require any changes.

The chapter 'Main concepts and relations' were discussed in more detailed manner. Text in this chapter should only describe the REST portion of the exercise work. We had described the purposes and operations of the IA Web API, but the purpose of this chapter is to focus on describing what concrete concepts the IA REST API deals with. Concrete concepts include for example image and annotation. From this paragraph, verbs should be reduced, i.e. the description of what is done should be reduced, and more descriptions should be made of which concepts are used,  i.e. more nouns should be used in the wiki description. Concepts that REST include are for example image, various annotations and labels, user information, date, and location.

The chapter 'API uses' described well the potential use case of the IA REST API attached to a third-party client. However, the ideas of the planned own clients and their description must be added to this chapter. Text should describe how REST API can be used, and what kind of client design the group has planned to on this course - for example 'Hate Speech Anno API Client' for annotation of hate speech images memes, and 'My Photo Label API Client' for collecting and labeling private photographs.

Good examples were found on the chapter 'Related work', so text did not need any changes.


### Action points
List here the actions points discussed with assistants

- The chapter 'Overview' did not need any changes.
- From the chapter 'Main concepts and relations' descriptions of uses and operations should be removed elsewhere, and new text should describe and focus on the concepts.
- Add project clients and their descriptions to the chapter 'API uses'.
- The chapter 'Related work' did not need any changes.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* DATE: 26.2.2021 12:30-13:00
* ASSISTANTS: Mika Oja

### Minutes
Summary of what was discussed during the meeting

The Entity Relationship (ER) -diagram is confusing, as nnly tables and their relationships shoul be displayed in the ER diagram — balls should be removed. Currently, the size of the work, database and models meet the resource requirements of the assignment.

Because SQLite was selected as database engine, enum cannot be used as parameter for models, although this could be done for SQL tables. When using SQLite, integer enum values and constraints are modified on code that defines server. On SQLite applications, when a request is received on the server, the condition statements check whether the value is within the allowed limits and whether the type is correct.

On API model tables, the  __init__ configurations are incorrectly encoded and unnecessary, because  SQLAlchemy automatically configures inits configurations by itself. Init codes should be removed  from  model configurations.

It was suggested that ImageContent and PhotoContent models could be combined into one single model since they are so similar. For example, when merging Content models, it is possible to add new field (eg. called private), where the sharing of images as web images or private photos is defined by boolean True/False parameter. This proposal is likely to be implemented using Boolean data type parameter. We also discussed about merging Annotation -models, but since there are a lot of differences on tables, this combination is unlikely to be done.

We discussed that as a part of testing we could try:

- It should be tested, if you destroy a user, Content data and Annotation data will also be deleted in connection with the user's data, or whether the user will only change to null.  When designing a database, you usually decide what happens when user deleted. In other words, in connection with the design, it must be decided whether all user-specific data (including image content and annotation data) will be deleted during user deletion, e.g.  null, or whether only user-specific data will be deleted as null.  One option is that images and annotations remain in the database, meaning that they cannot be discarded from the database when the user leaves. The last option is most likely to be implemented.
- Test the functionality of database and database cells in various update situations.
- Test that the database allows annotation data to be altered so that the entire annotation table is updated, deleted, or added at once per user, if possible.

We discussed shortly about testing strategies. It was mentioned that the method used so far to test the database and code is useful, but laborious when pytest testing has not been utilized. It was recommended that we should learn how to use the pytest. We also discussed the fact that testing can be improved and developed throughout the assignment work. The results will be assessed only in the end of the course.


### Action points
List here the actions points discussed with assistants

- Define new and more visual ER diagram
- Remove __init__ definitions from API -models
- Merge ImageContent and PhotoContent -models
- Add boolean data parameter for work related ImageContent and private PhotoContent data
- More test cases can be created as the course progress further
- We should learn how to use pytest during the course

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*



## Meeting 3.
* DATE: 24.3.2021 12:00-12:30 with Mika, and later some additional discussion with Iván
* ASSISTANTS: Mika Oja, Iván Sánchez Milara

### Minutes
Summary of what was discussed during the meeting

The meeting covered resource and request tables, state diagrams and apiary documentation compiled during API design.

The state diagram and resource tables are missing resources of one photo and one image. The ImageContent resource should be removed from the state diagram, and replaced with Photo and Image resources. In state diagram photos-all and images-all arrows should be corrected so that they point to the right direction.

Resources of designed API are not in correct order. The tables are missing single image and photo resources, which means that you must add both 'photo' resource and 'photos\photo' resource, as well as suitable links to the tables. In addition, you should add single photoannotation and imageannotation resources to the table. The annotation must be located at the end of a path where the image has been recognized. The image is related with the user, and the annotation is related both to the image and the user.

The resource request table contains too many POST requests. Unnecessary POST requests should be deleted, and requests should be reviewed once again after the resources have been defined correctly.

During Apiary review, it was found that the mason script style is quite well under control.

We discussed the API's general policy. The API takes the pictures individually to process from a folder on your computer, that is, the pictures are added one at a time to the API. The folder must be defined by a client, and the client goes through the folder, uploading one image at a time. A folder is always explicitly downloaded over the Web one file at a time — an entire folder cannot be downloaded at once for web security reasons.

During an annotation, the photo is identified by the photo URL, meaning that the photo URL will contain an ID, and after the annotation is generated, the photo URL contains both the image ID and the annotation ID.

Logging in is a state, so the user key always goes along with the URL address, and this should be shown also in the defined resource table.

During final discussion, it was agreed that in coursework , API testing can be done only on one side of the API, i.e. only for photoannotation part in order to to reduce the workload of coursework.

### Action points
List here the actions points discussed with assistants*

-	make corrections to errors on resources and resource urls
-	make corrections to errors on state diagram
-	make corrections to errors on resource request table
-	make corrections to errors on apiary documentation

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*




## Meeting 4.
* DATE: 5.5.2021 11:00 - 11:20 with Mika
* ASSISTANTS: Mika Oja

### Minutes
Summary of what was discussed during the meeting

Minimum requirement: for 5 resources, each method 2 times all together to be used

db_test was OK like it is now
    o	pytest coverage cannot be used for database

Resource_test must be further developed. Resource.py has still faults in it. Need to resolve the faults in resource.py, so that resource_test can be run without errors, and so that resource_test coverage will achieve accepted min level
    o	Resource test coverage: minimum coverage  85 % (see min requirements)

-	Asked and confirmed: All directory/file paths must be relative (db_test has two D-path to correct)

-	Asked and confirmed: client no need to test

### Action points
List here the actions points discussed with assistants*

Check minimum requirements and Constraints flom Lovelace:
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/pwp-project-work-assignment/#minimum-requirements-and-constraints

Resource_test need further development to gain higher test coverage.

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

