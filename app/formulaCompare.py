from sympy import *
from sympy.parsing.latex import parse_latex

def normalize_formula(expr):
    return latex(simplify(parse_latex(expr)))

def build_tree(expr):
    """
    Рекурсивно строит дерево операций с использованием .args.
    """
    if not expr.args:  # Если нет подвыражений, это лист
        return str(expr)
    
    # Узел дерева — операция или функция
    return (expr.func, [build_tree(arg) for arg in expr.args])

def flatten_tree(tree):
    """
    Разворачивает дерево в плоский список.
    """
    if isinstance(tree, str):
        return [tree]
    root, children = tree
    flat_list = [root]
    for child in children:
        flat_list.extend(flatten_tree(child))
    return flat_list


def compare_trees(tree1, tree2):
    """
    Рекурсивно сравнивает два дерева операций.
    Возвращает совпадающие операции и подвыражения.
    """
    if isinstance(tree1, str) or isinstance(tree2, str):
        # Если один из узлов — лист, сравниваем напрямую
        return ([], [tree1] if tree1 == tree2 else [], 0)

    root1, children1 = tree1
    root2, children2 = tree2

    # Сравниваем корневые операции
    common_operations = []
    common_subexpressions = []
    if root1 == root2:
        common_operations.append(root1)

        # Если всё поддерево совпадает, добавляем его как совпадающее подвыражение
        if children1 == children2:
            common_subexpressions.append(tree1)

    # Сравниваем поддеревья
    for sub_tree1, sub_tree2 in zip(children1, children2):
        sub_ops, sub_exprs, _ = compare_trees(sub_tree1, sub_tree2)
        common_operations.extend(sub_ops)
        common_subexpressions.extend(sub_exprs)

    # Разворачиваем деревья для расчета общего количества узлов
    flat_tree1 = flatten_tree(tree1)
    flat_tree2 = flatten_tree(tree2)
    common_nodes = set(flat_tree1).intersection(flat_tree2)

    # Процент совпадения
    total_nodes = max(len(flat_tree1), len(flat_tree2))
    similarity = (len(common_nodes) / total_nodes) * 100 if total_nodes > 0 else 0

    return common_operations, common_subexpressions, similarity


def subtree_to_expr(tree, parent_expr=None):
    """
    Преобразует поддерево обратно в выражение SymPy.
    """

    if isinstance(tree, str):
        if parent_expr is None:
            return
        if tree.isdigit():  # Целое число
            return Integer(int(tree))
        return Symbol(tree)  # Переменная

    operation, children = tree
    children_exprs = [subtree_to_expr(child, operation) for child in children]

    return operation(*children_exprs)


def compare_formula_trees(formula1, formula2):
    try:
        # Парсим формулы из LaTeX и упрощаем
        expr1 = simplify(parse_latex(formula1))
        expr2 = simplify(parse_latex(formula2))

        # expr1 = parse_latex(formula1).canonical
        # expr2 = parse_latex(formula2).canonical

        expr1_norm, new_symbols = normalize_variables(expr1)
        expr2_norm, _ = normalize_variables(expr2)

        # print(expr1)
        print(expr2)

        # Строим деревья операций
        tree1 = build_tree(expr1_norm)
        tree2 = build_tree(expr2_norm)

        # Сравниваем деревья
        common_operations, common_subexpressions, similarity = compare_trees(tree1, tree2)

        new_symbols = {v: k for k, v in new_symbols.items()}

        # Преобразуем совпадающие подвыражения в LaTeX
        common_expressions_latex = []
        for sub_tree in common_subexpressions:
            expr = subtree_to_expr(sub_tree)
            if expr is not None:
                expr = expr.subs(new_symbols)
                common_expressions_latex.append(latex(expr))

        return {
            # "общие операции": common_operations,
            "normalized": latex(expr1),
            "finded": formula2,
            "similarity": 0,
            "commonExpressions": common_expressions_latex,
        }

    except Exception as e:
        return {"ошибка": str(e)}
    
def normalize_variables(sympy_expr):
    """
    Приводит все переменные формулы к унифицированному виду (x1, x2, ...).
    """
    try:
        # Извлечение символов из выражения
        sorted_symbols = sorted(sympy_expr.free_symbols, key=lambda s: s.name)

        # Создание нового набора унифицированных переменных
        new_symbols = {sym: symbols(f"x{i+1}") for i, sym in enumerate(sorted_symbols)}

        # Замена старых переменных на новые
        normalized_expr = sympy_expr.subs(new_symbols)
        return normalized_expr, new_symbols
    except Exception as e:
        print(f"Ошибка при нормализации переменных: {e}")
        return None