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
    if '=' in expr:
        return latex(parse_latex(expr).canonical)
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

def extract_subtrees(tree):
    """
    Составляет все поддеревья исходного дерева

    Args:
        tree (list): дерево

    Returns:
        Список поддеревьев
    """
    subtrees = []  # Список для хранения всех поддеревьев
    stack = [tree]  # Стек для обхода узлов дерева

    while stack:
        node = stack.pop()

        if isinstance(node, str):
            # Если узел — строка (либо число, либо переменная), ничего не добавляем в subtrees
            continue

        # Добавляем текущее поддерево в список
        subtrees.append(sympify(subtree_to_expr(node)))

        # Узел содержит операцию и дочерние элементы
        operation, children = node

        # Добавляем дочерние элементы в стек
        stack.extend(children)

    return subtrees

def compare_subtrees(subtrees1, subtrees2, symbols):
    """
    Сравнивает поддеревья

    Args:
        subtrees1 (list): список поддеревьев
        subtrees2 (list): список поддеревьев

    Returns:
        Совпадающие выражения
        Процент совпадения
    """
    if len(subtrees2) == 0: return [], 0
    similarity = 0
    common_expressions = []
    for subtree in subtrees1:
        if subtree in subtrees2:
            similarity += 1
            common_expressions.append(latex(subtree.subs(symbols)))
    return common_expressions, (similarity / len(subtrees2)) * 100


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
        expr1 = None
        expr2 = None

        if '=' in formula1:
            expr1 = parse_latex(formula1).canonical
        else:
            expr1 = expand(simplify(parse_latex(formula1)))

        if '=' in formula2:
            expr2 = parse_latex(formula2).canonical
        else:
            expr2 = expand(simplify(parse_latex(formula2)))

        # Приводим переменные к единому формату
        expr1_norm, new_symbols = normalize_variables(expr1)
        expr2_norm, _ = normalize_variables(expr2)

        # Строим деревья операций
        tree1 = build_tree(expr1_norm)
        tree2 = build_tree(expr2_norm)

        new_symbols = {v: k for k, v in new_symbols.items()}

        subtrees1 = extract_subtrees(tree1)
        subtrees2 = extract_subtrees(tree2)

        expr1_from_tree = latex(simplify(subtree_to_expr(tree1)).subs(new_symbols))

        common_subexpressions, similarity = compare_subtrees(subtrees1, subtrees2, new_symbols)

        return {
            "normalized": latex(expr1),
            "finded": formula2,
            "similarity": calculate_similarity(expr1_from_tree, common_subexpressions),
            "commonExpressions": common_subexpressions
        }

    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    # formula1 = r"a^2 + 2ab"
    # formula2 = r"x^2 + 2xy + y^2"

    # formula1 = r"\sqrt{32+x^2}+x"
    # formula2 = r"\sqrt{32+x^2}"

    # formula1 = r"888"
    # formula2 = r"888"

    # formula1 = r"(a + b)^2 = a^2 + 2ab + b^2"
    # formula2 = f"a^2 - b^2 = (a - b)(a + b)"

    formula1 = r"f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x-a)^n + \cdots"
    formula2 = r"f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots + \frac{f^{(n)}(a)}{n!}(x-a)^n + \cdots"

    result = compare_formula_trees(formula1, formula2)
    for key, value in result.items():
        print(f"{key}: {value}")