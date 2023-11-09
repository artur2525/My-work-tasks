import json


def convert_tree_to_json(tree, feature_names=None, node_index=0):
    """hello kitty"""
    tree = tree.tree_
    feature_names = feature_names or [
        f"feature_{i}" for i in range(tree.n_features)]

    def recurse(node):
        if tree.children_left[node] != tree.children_right[node]:
            feature_index = tree.feature[node]
            threshold = round(tree.threshold[node], 4)
            left = recurse(tree.children_left[node])
            right = recurse(tree.children_right[node])

            return (f'{{ "feature_index": {feature_index},'
                    f' "threshold": {threshold},'
                    f'"left": {left}, "right": {right} }}')

        else:
            class_label = int(tree.value[node].argmax())

            return f'{{ "class": {class_label} }}'

    tree_str = recurse(node_index)
    return tree_str


def generate_sql_query(tree_json_str: str, feature_names: list) -> str:
    def parse_json(node_str):
        node = eval(str(node_str))  # Используем eval для разбора JSON-строки
        if "feature_index" in node:
            feature_name = feature_names[node["feature_index"]]
            threshold = node["threshold"]
            left = parse_json(node["left"])
            right = parse_json(node["right"])
            return f"CASE WHEN {feature_name} > {threshold} THEN {right} ELSE {left} END"
        elif "class" in node:
            class_label = class_labels[node["class"]]
            return str(class_label)
        else:
            raise ValueError("Неверный формат JSON")

    class_labels = {0: "0", 1: "1"}  # Замените на ваше представление классов
    where_clause = parse_json(tree_json_str)
    sql_query = f"SELECT {where_clause} AS CLASS_LABEL"
    return sql_query

