import React from 'react';
import {Composition, getInputProps} from 'remotion';
import {EpisodeVideo, EpisodeProps, FPS} from './EpisodeVideo';

const fallbackProps: EpisodeProps = {
  canvas: {width: 1080, height: 1920, fps: FPS},
  draftDurationSeconds: 90,
  scenes: [],
};

export const Root: React.FC = () => {
  const props = {...fallbackProps, ...getInputProps<EpisodeProps>()};
  const durationInFrames = Math.max(1, Math.ceil((props.draftDurationSeconds || 90) * FPS));

  return (
    <Composition
      id="ThreeMinuteFuture"
      component={EpisodeVideo}
      durationInFrames={durationInFrames}
      fps={FPS}
      width={props.canvas?.width || 1080}
      height={props.canvas?.height || 1920}
      defaultProps={props}
    />
  );
};
