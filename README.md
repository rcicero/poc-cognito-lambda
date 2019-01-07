# poc-cognito-lambda

1 - Crie um bucket no s3 da sua conta na AWS.

2 - Coloque o nome do bucket criado no arquivo application.yml no lugar de {Bucket}

3 - Entre na pasta e crie um arquivo zip com o comando "zip -r9 ../function.zip ."

4 - Faça upload do arquivo zip para o s3

5- Crie uma stack no CloudFormation com o template do arquivo application.yml