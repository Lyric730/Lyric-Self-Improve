import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const FPS = 30;

type Scene = {
  id: string;
  type: 'cover' | 'story' | 'outro';
  title?: string;
  source?: string;
  image: string;
  audio?: string | null;
  voiceover?: string;
  durationSeconds: number;
  transitionSeconds?: number;
};

export type EpisodeProps = {
  canvas?: {width: number; height: number; fps: number};
  draftDurationSeconds?: number;
  account?: string;
  scenes: Scene[];
};

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

const frames = (seconds: number) => Math.max(1, Math.round(seconds * FPS));

const sceneStartFrames = (scenes: Scene[]) => {
  let cursor = 0;
  return scenes.map((scene) => {
    const start = cursor;
    cursor += frames(scene.durationSeconds + (scene.transitionSeconds || 0));
    return start;
  });
};

const BackgroundPlate: React.FC<{scene: Scene}> = ({scene}) => {
  return (
    <AbsoluteFill style={{background: '#070807', overflow: 'hidden'}}>
      <Img
        src={staticFile(scene.image)}
        style={{
          position: 'absolute',
          inset: -80,
          width: 'calc(100% + 160px)',
          height: 'calc(100% + 160px)',
          objectFit: 'cover',
          filter: 'blur(26px) brightness(0.28) saturate(0.8)',
          transform: 'scale(1.08)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'linear-gradient(180deg, rgba(0,0,0,.55), rgba(0,0,0,.18) 35%, rgba(0,0,0,.72)), repeating-linear-gradient(0deg, rgba(207,255,0,.06) 0 1px, transparent 1px 28px), repeating-linear-gradient(90deg, rgba(0,229,255,.035) 0 1px, transparent 1px 36px)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -160,
          top: 1330,
          width: 1440,
          height: 190,
          background: 'rgba(255, 44, 122, .18)',
          transform: 'rotate(-17deg)',
        }}
      />
    </AbsoluteFill>
  );
};

const SceneCard: React.FC<{scene: Scene; sceneFrame: number}> = ({scene, sceneFrame}) => {
  const isCover = scene.type !== 'story';
  const imageWidth = isCover ? 970 : 920;
  const imageHeight = isCover ? 970 : 1206;
  const top = isCover ? 330 : 192;
  const intro = spring({frame: sceneFrame, fps: FPS, config: {damping: 28, stiffness: 90}});
  const zoom = interpolate(sceneFrame, [0, frames(scene.durationSeconds)], [1.012, 1.045], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const opacity = clamp(interpolate(sceneFrame, [0, 10], [0, 1]), 0, 1);

  return (
    <div
      style={{
        position: 'absolute',
        left: (1080 - imageWidth) / 2,
        top,
        width: imageWidth,
        height: imageHeight,
        transform: `translateY(${(1 - intro) * 18}px) scale(${zoom})`,
        opacity,
        boxShadow: '18px 24px 0 rgba(255,44,122,.18), -10px -10px 0 rgba(0,229,255,.22)',
        overflow: 'hidden',
        border: '1px solid rgba(244,241,232,.28)',
        background: '#0b0c0b',
      }}
    >
      <Img src={staticFile(scene.image)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </div>
  );
};

const Caption: React.FC<{scene: Scene; sceneFrame: number}> = ({scene, sceneFrame}) => {
  const show = scene.type === 'story';
  if (!show) return null;
  const opacity = clamp(interpolate(sceneFrame, [18, 30], [0, 1]), 0, 1);
  return (
    <div
      style={{
        position: 'absolute',
        left: 74,
        right: 74,
        bottom: 156,
        opacity,
        background: '#f4f1e8',
        color: '#10110f',
        borderLeft: '16px solid #cfff00',
        boxShadow: '10px 10px 0 #ff2c7a',
        padding: '22px 28px 24px',
        fontFamily: '"Microsoft YaHei", "PingFang SC", Arial, sans-serif',
        fontWeight: 900,
        fontSize: scene.title && scene.title.length > 14 ? 42 : 50,
        lineHeight: 1.08,
      }}
    >
      {scene.title}
      {scene.source ? (
        <div style={{marginTop: 12, fontSize: 22, color: '#363931', fontWeight: 700}}>{scene.source}</div>
      ) : null}
    </div>
  );
};

const TransitionFlash: React.FC<{sceneFrame: number}> = ({sceneFrame}) => {
  const opacity = clamp(interpolate(sceneFrame, [0, 4, 12], [0.55, 0.18, 0]), 0, 0.55);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        opacity,
        background:
          'linear-gradient(90deg, transparent 0 8%, rgba(207,255,0,.95) 8% 14%, transparent 14% 43%, rgba(0,229,255,.9) 43% 52%, transparent 52% 100%)',
        mixBlendMode: 'screen',
      }}
    />
  );
};

const SceneView: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <BackgroundPlate scene={scene} />
      <SceneCard scene={scene} sceneFrame={frame} />
      <Caption scene={scene} sceneFrame={frame} />
      {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
      <TransitionFlash sceneFrame={frame} />
    </AbsoluteFill>
  );
};

export const EpisodeVideo: React.FC<EpisodeProps> = ({scenes}) => {
  const {durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const starts = sceneStartFrames(scenes || []);
  if (!scenes?.length) {
    return <AbsoluteFill style={{background: '#070807'}} />;
  }
  return (
    <AbsoluteFill style={{background: '#070807'}}>
      {scenes.map((scene, i) => (
        <Sequence key={scene.id} from={starts[i]} durationInFrames={frames(scene.durationSeconds + (scene.transitionSeconds || 0))}>
          <SceneView scene={scene} />
        </Sequence>
      ))}
      <div
        style={{
          position: 'absolute',
          left: 0,
          bottom: 0,
          height: 8,
          width: `${(frame / durationInFrames) * 100}%`,
          background: '#cfff00',
        }}
      />
    </AbsoluteFill>
  );
};
