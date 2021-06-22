#!/bin/sh -l

if ! [ -z "$STAGE" ]
then
      stageSubCommand="--stage $STAGE"
fi

if ! [ -z "$GOBLET_PATH" ]
then
    cd "$GOBLET_PATH"
fi

command="goblet deploy --project $PROJECT --location $LOCATION $stageSubCommand"

eval $command