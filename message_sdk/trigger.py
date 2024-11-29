"""
This file contains the trigger system for message sdk
"""

import operator


def _get_trigger_value(operand, before, after):
    """
    This function return the value of the trigger,
    if operator provided is a trigger, else return operator itself
    """
    return operand(before, after)


def _operator(op):
    """
    Wrapper for operators to be used in trigger system
    """

    def inner(first_operand, second_operand, before, after):
        return op(
            _get_trigger_value(first_operand, before, after),
            _get_trigger_value(second_operand, before, after),
        )

    inner.__name__ = op.__name__
    return inner


class TriggerOperatorsMixins:
    """
    This class defines all the overloaded operators for trigger.
    Used to incorporate triggers with python operators
    """

    def __call__(self, before, after):
        return NotImplementedError(
            "This class definition must be provided in child class"
        )

    def __eq__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__eq__))

    def __ne__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__ne__))

    def __lt__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__lt__))

    def __le__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__le__))

    def __gt__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__gt__))

    def __ge__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__ge__))

    def __add__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__add__))

    def __radd__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__add__))

    def __sub__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__sub__))

    def __rsub__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__sub__))

    def __mul__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__mul__))

    def __rmul__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__mul__))

    def __truediv__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__truediv__))

    def __rtruediv__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__truediv__))

    def __mod__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__mod__))

    def __rmod__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__mod__))

    def __pow__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, _operator(operator.__pow__))

    def __rpow__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, _operator(operator.__pow__))

    def __and__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, AND)

    def __rand__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, AND)

    def __or__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, OR)

    def __ror__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, OR)

    def __xor__(self, second_operand):
        return BinaryChainTrigger(self, second_operand, XOR)

    def __rxor__(self, second_operand):
        return BinaryChainTrigger(second_operand, self, XOR)

    def __contains__(self, second_operand):
        return BinaryChainTrigger(
            self, second_operand, _operator(operator.__contains__)
        )

    def __abs__(self):
        return UnaryChainTrigger(self, operator.__abs__)

    def __invert__(self):
        raise NotImplementedError("Invert is deprecated in python3.")

    def __bool__(self):
        raise NotImplementedError("Bool is not suitable for chaining")


class TriggerBase(TriggerOperatorsMixins):
    """
    Base class for the whole trigger system
    """

    def __init__(self, field_name: None) -> None:
        self.field_name = field_name

    def __repr__(self):
        return f"{self.__class__.__name__}(field_name={self.field_name})"

    def validate_operation(self, operation):
        """
        This method is used to validate the operation performed (create, update, delete)
        """
        return NotImplementedError(
            "This class definition must be provided in child class"
        )


class BinaryChainTrigger(TriggerBase):
    """
    This class is used to define binary operation with trigger and other operands.
    """

    def __init__(self, first_operand, second_operand, op=None):
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.operator = op

    def __call__(self, before, after):
        return self.operator(self.first_operand, self.second_operand, before, after)

    def __repr__(self):
        return f"{self.__class__.__name__}(first_operand={self.first_operand}, second_operand={self.second_operand}, op={self.operator})"


class UnaryChainTrigger(TriggerBase):
    """
    This class is used to define unary operation with trigger and other operands.
    """

    def __init__(self, operand, op=None):
        self.operand = operand
        self.operator = op

    def __call__(self, before, after):
        op = _get_trigger_value(self.operand, before, after)
        if not self.operator:
            return op

        return self.operator(op)

    def __repr__(self):
        """
        Returns a string representation of the UnaryChainTrigger
        """
        return f"{self.__class__.__name__}(operand={self.operand}, op={self.operator})"


class Before(TriggerBase):
    """
    Class used to return the field value before the update
    """

    def __call__(self, before, after):
        """
        Returns the field value before the update
        """
        return before[self.field_name]

    def __repr__(self):
        """
        Returns a string representation of the Before trigger
        """
        return f"{self.__class__.__name__}(field_name={self.field_name})"

    def validate_operation(self, operation):
        """
        This method is used to validate the operation performed (create, update, delete)
        """
        if operation == "create":
            return False
        return True


class After(TriggerBase):
    """
    Class used to return the field value after the update
    """

    def __call__(self, before, after):
        """
        Returns the field value after the update
        """
        return after[self.field_name]

    def __repr__(self):
        return f"{self.__class__.__name__}(field_name={self.field_name})"

    def validate_operation(self, operation):
        """
        This method is used to validate the operation performed (create, update, delete)
        """
        if operation == "delete":
            return False
        return True


def AND(first_operand, second_operand, before, after):
    """
    Returns the AND of the two operands
    """
    first_operand = bool(_get_trigger_value(first_operand, before, after))
    if not first_operand:
        return first_operand

    return first_operand & bool(_get_trigger_value(second_operand, before, after))


def OR(first_operand, second_operand, before, after):
    """
    Returns the OR of the two operands
    """
    first_operand = bool(_get_trigger_value(first_operand, before, after))
    if first_operand:
        return first_operand

    return first_operand | bool(_get_trigger_value(second_operand, before, after))


def XOR(first_operand, second_operand, before, after):
    """
    Returns the XOR of the two operands
    """
    return bool(_get_trigger_value(first_operand, before, after)) ^ bool(
        _get_trigger_value(second_operand, before, after)
    )
