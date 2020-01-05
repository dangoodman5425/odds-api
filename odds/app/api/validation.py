from marshmallow import Schema, fields


class CreateOddsSchema(Schema):

    """ /VERSION/odds - POST
    """
    odds_name = fields.Str(required=True)
    odds_type = fields.Str(required=True)
    snippet = fields.Str(required=True)
    image_uuid = fields.Str()


class UpdateOddsSchema(Schema):

    """ /VERSION/odds/<odds_id> - PUT
    """
    pass


class CreateOddsFilterSchema(Schema):

    """ /VERSION/odds/<odds_uuid> - POST
    """
    filter_type = fields.Str(required=True)
    filter_name = fields.Str(required=True)


class UpdateOddsFilterSchema(Schema):

    """ /VERSION/odds/<odds_uuid> - PUT
    """
    pass
