# Random notes

https://github.com/n-y-z-o/nyzoVerifier/blob/master/src/main/java/co/nyzo/verifier/Node.java


private static final int communicationFailureInactiveThreshold = 6;

private byte[] identifier;                    // wallet public key (32 bytes)
private byte[] ipAddress;                     // IPv4 address, stored as bytes to keep memory predictable (4 bytes)
private int portTcp;                          // TCP port number
private int portUdp;                          // UDP port number, if available
private long queueTimestamp;                  // this is the timestamp that determines queue placement -- it is
                                              // when the verifier joined the mesh or when the verifier was last
                                              // updated
private long inactiveTimestamp;               // when the verifier was marked as inactive; -1 for active verifiers
private long communicationFailureCount;       // consecutive communication failures before marking inactive


communicationFailureCount is inc by markFailedConnection(), reset by markSuccessfulConnection()

markFailedConnection is called by NodeManager, from its own markFailedConnection(), called by  Message:
https://github.com/n-y-z-o/nyzoVerifier/blob/75786060a822443154bcdaaa371fe8696d54a201/src/main/java/co/nyzo/verifier/Message.java#L213

markSuccessfulConnection is called by NodeManager.
Either by a successful message fetch... either from updateNode at https://github.com/n-y-z-o/nyzoVerifier/blob/75786060a822443154bcdaaa371fe8696d54a201/src/main/java/co/nyzo/verifier/NodeManager.java#L99
That one is called from a successful response to nodejoin, **or** a NodeJoinV2_43.

https://github.com/n-y-z-o/nyzoVerifier/blob/75786060a822443154bcdaaa371fe8696d54a201/src/main/java/co/nyzo/verifier/MeshListener.java#L506


