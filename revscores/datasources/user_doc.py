from .datasource import datasource_processor
from .revision_metadata import revision_metadata


@datasource_processor(['session', revision_metadata])
def user_doc(session, revision_metadata):
    user_docs = session.users.query(
            users={revision_metadata.user_text},
            properties={'blockinfo', 'implicitgroups', 'groups', 'registration',
                        'emailable', 'editcount', 'gender'})
    
    user_docs = list(user_docs)
    if len(user_docs) >= 1:
        return user_docs[0]
    else:
        return None
