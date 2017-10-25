import json
import time

from charms import reactive

from spcharms import service_hook

def rdebug(s):
    with open('/tmp/storpool-charms.log', 'a') as f:
        print('{tm} [storpool-service-provides] {s}'.format(tm=time.ctime(), s=s), file=f)

class StorPoolServicePeer(reactive.RelationBase):
    scope = reactive.scopes.UNIT

    @reactive.hook('{peers:storpool-service}-relation-{joined,changed}')
    def peer_changed(self):
        rdebug('relation-joined/changed invoked')
        try:
            conv = self.conversation()
            data = conv.get_remote('storpool_service')
            if data is None:
                rdebug('- no service data yet, sending ours then')
                (state, _) = service_hook.get_state()
                rdebug('- just making sure we have "-local" in the state array: {have}'.format(have='-local' in state))
                conv.set_remote('storpool_service', json.dumps(state['-local']))
                rdebug('- done with this hook, it seems')
                return
            data = json.loads(data)
            if not isinstance(data, dict):
                rdebug('- hmmm, deserialized the service data, but not a dictionary - "{t}" instead'.format(t=type(data).__name__))
                return

            rdebug('- we got some data from the other side: {data}'.format(data=data))
            changed = service_hook.handle(self, True, data, rdebug=rdebug)
            if changed:
                rdebug('- looks like something changed when we received the data, sending ours across')
                (state, _) = service_hook.get_state()
                rdebug('- got full state: {state}'.format(state=state))
                conv.set_remote('storpool_service', json.dumps(state['-local']))
                rdebug('- looks fine')
        except Exception as e:
            rdebug('could not complete the relation joined/changed actions: {e}'.format(e=e))

    @reactive.hook('{peers:storpool-service}-relation-departed')
    def peer_departed(self):
        rdebug('relation-departed')
        try:
            service_hook.handle(self, False, None, rdebug=rdebug)
        except Exception as e:
            rdebug('could not complete the relation departed actions: {e}'.format(e=e))
