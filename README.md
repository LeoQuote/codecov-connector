# codecov-connector
codecov depends on upload token to upload coverage report , while
codecov does not support global upload token in self-host instances.

this little web app provide a single api that can retrieve upload token for given org and repo, 
making it possible for you to upload coverage report to any rpeo

# installation


# usage
1. get upload token for given repo `curl <your-service>/<org>/<repo>`
2. upload coverage with `codecov -t <token>`

