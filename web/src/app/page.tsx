'use client';

import { useEffect, useMemo, useState } from 'react';
import { Room, RoomEvent } from 'livekit-client';
import { motion } from 'motion/react';
import { RoomAudioRenderer, RoomContext, StartAudio } from '@livekit/components-react';
import { toast } from 'sonner';
// import { SessionView } from '@/components/session-view';
import { Landing } from '@/components/landing';
// import useConnectionDetails from '@/hooks/useConnectionDetails';
import { constants } from '@/lib/constants';

const MotionWelcome = motion.create(Landing);
// const MotionSessionView = motion.create(SessionView);

const App = () => {
  
  const room = useMemo(() => new Room(), []);
  const [sessionStarted, setSessionStarted] = useState(false);
  // const { refreshConnectionDetails, existingOrRefreshConnectionDetails } =
  //   useConnectionDetails(appConfig);

  useEffect(() => {
    const onDisconnected = () => {
      setSessionStarted(false);
      // refreshConnectionDetails();
    };
    const onMediaDevicesError = (error: Error) => {
      toast(' Encountered an error with your media devices');
    };
    room.on(RoomEvent.MediaDevicesError, onMediaDevicesError);
    room.on(RoomEvent.Disconnected, onDisconnected);
    return () => {
      room.off(RoomEvent.Disconnected, onDisconnected);
      room.off(RoomEvent.MediaDevicesError, onMediaDevicesError);
    };
  }, [room]);

  useEffect(() => {
    let aborted = false;
    if (sessionStarted && room.state === 'disconnected') {
      Promise.all([
        room.localParticipant.setMicrophoneEnabled(true, undefined, {
          preConnectBuffer: constants.isPreConnectBufferEnabled,
        }),
        // existingOrRefreshConnectionDetails().then((connectionDetails) =>
        //   room.connect(connectionDetails.serverUrl, connectionDetails.participantToken)
        // ),
      ]).catch((error) => {
        if (aborted) {
          return;
        }

        toast('There was an error connecting to the agent');
      });
    }
    return () => {
      aborted = true;
      room.disconnect();
    };
  }, [room, sessionStarted]);

  return (
    <main>
      <MotionWelcome
        key="welcome"
        onStartCall={() => setSessionStarted(true)}
        disabled={sessionStarted}
        initial={{ opacity: 1 }}
        animate={{ opacity: sessionStarted ? 0 : 1 }}
        transition={{ duration: 0.5, ease: 'linear', delay: sessionStarted ? 0 : 0.5 }}
      />

      <RoomContext.Provider value={room}>
        <RoomAudioRenderer />
        <StartAudio label="Start Audio" />
        {/* --- */}
        {/*<MotionSessionView
          key="session-view"
          disabled={!sessionStarted}
          sessionStarted={sessionStarted}
          initial={{ opacity: 0 }}
          animate={{ opacity: sessionStarted ? 1 : 0 }}
          transition={{
            duration: 0.5,
            ease: 'linear',
            delay: sessionStarted ? 0.5 : 0,
          }}
        />*/}
      </RoomContext.Provider>
    </main>
  );
}

export default App;
