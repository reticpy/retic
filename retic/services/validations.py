"""Validation services"""

def validate_obligate_fields(fields: any = None):
    """Validate if a list of obligate params are valid    

    :param fields: object that contains all params that are obligate, 
    these values can be arrays or simple values."""

    '''You can use the following example:

    _validate = validate_obligate_fields({     
        u'files': req.files.get("files", None)         
    })

    if _validate["valid"] is False:        
        return res.bad_request(            
            error_response(                
                "The param {} is necesary.".format(_validate["error"])                
            )            
        )
    '''
    if not fields:
        raise ValueError("error: A value for fields is necessary.")

    for field in fields:
        _item = fields.get(field, None)
        if _item == None \
                or (isinstance(_item, str) and _item == "") \
                or (isinstance(_item, list) and not _item):
            return {
                u'valid': False,
                u'error': field
            }
    return {
        u'valid': True,
        u'error': None
    }
