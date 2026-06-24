# JuniorSwarm RPC layer - extends BitNet-mlx swarm/rpc.py patterns

class JuniorSwarmRPC:
    """Structured agent communication for JuniorSwarm."""
    def __init__(self):
        self.message_log = []

    def send(self, sender: str, receiver: str, msg_type: str, payload: dict):
        self.message_log.append({"from": sender, "to": receiver, "type": msg_type, "payload": payload})
        return True