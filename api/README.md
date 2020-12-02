# EMS Micro Services

This repository contains prototype API for correcting a gps trajectory distance measure
This is a prototype and should not be used for production
# Important
current assumptions:
- uniform sampling rate (same time step between all observations)
- no missing measurements
    
## Requirements
- A recent version of Docker 
  - See https://docs.docker.com/
- The port 5000  on your machine need to be available for binding 
## Usage
To build and run the server you can either use
``` shellsession
$> docker build -t intigo-gps:latest .
$> docker run -d -p 5000:5000 intigo-gps
```

## API documentation
You start by posting a trajectory to /
the request format is :
``` shellsession
POST http://127.0.0.1:5000/
{
    "longitude": [float],
    "latitude": [float],
    Optional("model_id"): str,
    Optional("method"): OneOf(METHODS),
    Optional("output"): OneOf(OUTPUT),
    Optional("distance_cutoff"): float,
    Optional("smoothing_factor"): float,
}

METHODS = ["filter", "smooth", "both"]
OUTPUT = ["distance", "path", "both"]
```
model_id is optional, if not supplied an id will be generated and returned
method to either use hard filtering, kalman smoothing or both (default: both)
output either only distance, only path or both (default both)
distance_cutoff hard filtering hyper-parameter (default 1000)
smoothing_factor kalman smoothing hyper-parameter (default 0.1)

Once a model is posted you can visualize the trajectory using 

``` shellsession
GET http://127.0.0.1:5000/model_id
```
where model_id is the id that you just posted 
``` shellsession
GET http://127.0.0.1:5000/tunis
```
is an example output

Model are saved to the history folder