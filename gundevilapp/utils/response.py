from flask import jsonify
from typing import Any, Dict, List, Optional, Union


class APIResponse:
  def __init__(self):
    self.DEFAULT_PAGE_SIZE = 10

  def success(
    self,
    data: Optional[Union[List, Dict, Any]] = None,
    message: str = "Success",
    code: int = 200,
    meta: Optional[Dict] = None,
    pagination: Optional[Dict] = None
  ):
    response = {
      "success": True,
      "message": message,
      "data": data
    }

    if meta:
      response['meta'] = meta

    if pagination:
      response['pagination'] = pagination

    return jsonify(response), code

  def error(
    self,
    message: str = "Error",
    code: int = 400,
    errors: Optional[Union[List, Dict]] = None
  ):
    response = {
      "success": False,
      "message": message
    }

    if errors:
      response["errors"] = errors

    return jsonify(response), code

  def paginate(
    self,
    query,
    page: int = 1,
    page_size: Optional[int] = None,
    schema=None,
    include_relationships: Optional[List[str]] = None,
  ):
    if page_size is None:
      page_size = self.DEFAULT_PAGE_SIZE

    paginated = query.paginate(
      page=page,
      per_page=page_size,
      error_out=False
    )

    # ! harus punya to_dict method disemua model biar bisa
    data = [item.to_dict(include_relationships=include_relationships) if hasattr(item, 'to_dict') else item
            for item in paginated.items]

    if schema:
      data = schema.dump(data, many=True)

    pagination = {
      "total_items": paginated.total,
      "total_pages": paginated.pages,
      "current_page": page,
      "page_size": page_size,
      "has_next": paginated.has_next,
      "has_prev": paginated.has_prev
    }

    return self.success(
      data=data,
      pagination=pagination
    )
