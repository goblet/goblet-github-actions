#!/bin/sh -l

if ! [ -z "$STAGE" ]
then
      stageSubCommand="--stage $STAGE"
fi

if ! [ -z "$GOBLET_PATH" ]
then
    cd "$GOBLET_PATH"
fi
config="{\"cloudfunction\":{\"environmentVariables\":{$1}}}"
command="goblet deploy --project $PROJECT --location $LOCATION $stageSubCommand --config $config"

eval $command