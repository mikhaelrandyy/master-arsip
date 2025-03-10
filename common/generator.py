import random
from sqlmodel.ext.asyncio.session import AsyncSession
from models.code_counter_model import CodeCounter
from common.enum import  CodeCounterEnum
import crud

async def generate_code(entity: CodeCounterEnum, db_session: AsyncSession | None = None) -> str:

    obj_current = await crud.code_counter.get_by_entity(entity=entity)

    code_counter = 1
    max_digit = 5  

    if obj_current is None:
        obj_in = CodeCounter(entity=entity, last=code_counter, digit=max_digit)
        await crud.code_counter.create(obj_in=obj_in, db_session=db_session)

        code = str(code_counter).zfill(max_digit)
        return f"{entity.value}-{code}"

    else:
        code_counter = obj_current.last + 1
        max_digit = obj_current.digit or max_digit
        max_value = 10 ** max_digit - 1

        if code_counter > max_value:
            max_digit += 1  

        obj_new = CodeCounter(entity=obj_current.entity, last=code_counter, digit=max_digit)
        await crud.code_counter.update(obj_current=obj_current, obj_new=obj_new, db_session=db_session)

        code = str(code_counter).zfill(max_digit)
        return f"{entity.value}-{code}"




    



