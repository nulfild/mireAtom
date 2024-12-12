from sympy import *
from sympy.parsing.latex import parse_latex
from difflib import SequenceMatcher

def normalize_formula(expr):
    """
    Нормализует выражение

    Args:
        expr (str): Выражение в формате latex

    Returns:
        Нормализованное выражние в формате latex
    """
    return latex(simplify(parse_latex(expr)))

def build_tree(expr):
    """
    Рекурсивно строит дерево операций с использованием .args

    Args:
        expr: Выражение в виде sympy объекта
    
    Returns:
        Рекурсивный вызов функции, возвращающий список, где первый элемент - это корень дерева, а второй - поддеревья
    """
    if not expr.args:  # Если нет подвыражений, это лист
        return str(expr)
    
    # Узел дерева — операция или функция
    return (expr.func, [build_tree(arg) for arg in expr.args])

def flatten_tree(tree):
    """
    Разворачивает дерево в плоский список

    Args:
        expr: Выражение в виде sympy объекта
    Return:
        flat_list (list): Развернутое дерево
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
    Рекурсивно сравнивает два дерева операций

    Args:
        tree1 (list): Дерево первого выражения
        tree2 (list): Дерево второго выражения

    Returns:
        common_operations (list): совпадающие операции
        common_subexpressions (list): совпадающие подвыражения
    """
    if isinstance(tree1, str) or isinstance(tree2, str):
        # Если один из узлов — лист, сравниваем напрямую
        return ([], [tree1] if tree1 == tree2 else [])

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
        sub_ops, sub_exprs = compare_trees(sub_tree1, sub_tree2)
        common_operations.extend(sub_ops)
        common_subexpressions.extend(sub_exprs)

    return common_operations, common_subexpressions


def subtree_to_expr(tree, parent_expr=None):
    """
    Преобразует поддерево обратно в выражение SymPy

    Args:
        tree: (list): Дерево выражения
        parent_expr: Корневое выражение в виде sympy объекта
    
    Returns:
        Выражение в виде sympy объекта
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


def calculate_similarity(formula, common_expressions):
    """
    Рассчет процента схожести формулы и совпадающих частей

    Args:
        formula (str): Выражение в формате latex
        common_expressions (list): Список совпадающих частей в формате latex

    Returns:
        similarity (float): Процент схожести
    """
    similarity = 0
    for common_expression in common_expressions:
        res = SequenceMatcher(a=formula, b=common_expression).ratio()
        # Находим максимальное похожее выражение и его возвращаем
        if res > similarity: similarity = res
    return similarity * 100


def normalize_variables(sympy_expr):
    """
    Приводит все переменные формулы к унифицированному виду (x1, x2, ...)

    Args:
        sympy_expr: Выражение в виде sympy объекта
    
    Returns:
        normalized_expr: Выражение в виде sympy объекта
        new_symbols (dict): Сопоставление символов
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


def compare_formula_trees(formula1, formula2):
    """
    Сравнение двух формул

    Args:
        formula1 (str): Выражение в формате latex
        formula2 (str): Выражение в формате latex

    Returns:
        Словарь, где описаны следующие элементы:
        normalized (str): Нормализованное выражение
        finded (str): Вторая формула
        similarity (float): Процент схожести
        commonExpressions (list): Список совпадающих частей
    """
    try:
        # Парсим формулы из LaTeX и упрощаем
        expr1 = simplify(parse_latex(formula1))
        expr2 = simplify(parse_latex(formula2))

        # expr1 = parse_latex(formula1).canonical
        # expr2 = parse_latex(formula2).canonical

        # Приводим переменные к единому формату
        expr1_norm, new_symbols = normalize_variables(expr1)
        expr2_norm, _ = normalize_variables(expr2)

        # Строим деревья операций
        tree1 = build_tree(expr1_norm)
        tree2 = build_tree(expr2_norm)

        # Сравниваем деревья
        common_operations, common_subexpressions = compare_trees(tree1, tree2)

        new_symbols = {v: k for k, v in new_symbols.items()}

        # Преобразуем совпадающие подвыражения в LaTeX
        common_expressions_latex = []
        for sub_tree in common_subexpressions:
            expr = subtree_to_expr(sub_tree)
            if expr is not None:
                expr = expr.subs(new_symbols)
                common_expressions_latex.append(latex(expr))

        return {
            "normalized": latex(expr1),
            "finded": formula2,
            "similarity": calculate_similarity(latex(expr1), common_expressions_latex),
            "commonExpressions": common_expressions_latex,
        }

    except Exception as e:
        return {"ошибка": str(e)}
    
if __name__ == "__main__":
    formula1 = r"a^2 + 2ab + b^2"
    formula2 = r"x^2 + 2xy + y^2"

    result = compare_formula_trees(formula1, formula2)
    for key, value in result.items():
        print(f"{key}: {value}")