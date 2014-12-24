from .datasource import datasource_processor


@datasource_processor(['rev_id', 'session'])
def rev_doc(rev_id, session):
    try:
        doc = session.revisions.get(rev_id=rev_id,
                                    properties={'ids', 'user', 'timestamp',
                                                'userid', 'comment', 'content',
                                                'flags', 'size'})
        return doc
    except KeyError:
        raise RevisionDocumentNotFound({'rev_id': rev_id})
