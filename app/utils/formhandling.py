from typing import List, Tuple, Any
from flask_wtf import Form


def extract_items_data(form: 'Form', attributes: List[str]) -> List[Tuple[Any]]:
    """
    Extracts data from individual items in a form and returns it as a list of tuples.

    Args:
        form (Form): The form containing the items.
        attributes (List[str]): The attributes to extract from each item.

    Returns:
        List[Tuple[Any]]: A list of tuples, where each tuple contains the extracted data
            from an item.
    """
    # Iterate over each item in the form.
    return [
        # Extract the data for each attribute from the item and create a tuple.
        tuple(getattr(item, attr).data for attr in attributes)
        for item in form.items
    ]
