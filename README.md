# aws-idp

Cloud-Native Intelligent Document Processing (IDP) and Retrieval-Augmented Generation (RAG) System using AWS and LangChain

1. User uploads file using presigned S3 URL
2. S3 triggers Lambda to start Textract job
3. Textract publishes result to SNS
4. SNS dispatches message to SQS
5. Lambda reads SQS and starts Step Functions
6. Step Functions:
   - saves Textract output
   - classifies document via Bedrock
   - extracts invoice fields
   - stores structured data in DynamoDB
   - creates embeddings and updates Pinecone
   - archives document
7. If confidence is low → SNS triggers manual review
8. FastAPI chat endpoint answers using RAG
