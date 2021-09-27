#!/bin/sh -l

if ! [ -z "$STAGE" ]
then
      stageSubCommand="--stage $STAGE"
fi

if ! [ -z "$GOBLET_PATH" ]
then
    cd "$GOBLET_PATH"
fi

if ! [ -z "$1" ]
then
    command="goblet deploy --project $PROJECT --location $LOCATION $stageSubCommand --config-from-json-string $1"
else
    command="goblet deploy --project $PROJECT --location $LOCATION $stageSubCommand"
fi

eval $command