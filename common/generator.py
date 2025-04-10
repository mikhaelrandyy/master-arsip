import random
from sqlmodel.ext.asyncio.session import AsyncSession
from models.code_counter_model import CodeCounter
from common.enum import  CodeCounterEnum
import crud
from datetime import datetime

async def generate_code(entity: CodeCounterEnum, db_session: AsyncSession | None = None) -> str:

    obj_current = await crud.code_counter.get_by_entity(entity=entity)

    code_counter = 1
    max_digit = 5  

    if obj_current is None:
        obj_in = CodeCounter(entity=entity, last=code_counter, digit=max_digit)
        await crud.code_counter.create(obj_in=obj_in, db_session=db_session)

        code = str(code_counter).zfill(max_digit)

        if CodeCounterEnum.MEMO:
            year = datetime.today().year
            month = datetime.today().month
            last_two_digit = str(year)[-2:]
            month_two_digit = f"{month:02d}"

            return f"{entity.value}-{last_two_digit}{month_two_digit}-{code}"

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

        if CodeCounterEnum.MEMO:
            year = datetime.today().year
            month = datetime.today().month
            last_two_digit = str(year)[-2:]
            month_two_digit = f"{month:02d}"

            return f"{entity.value}-{last_two_digit}{month_two_digit}-{code}"
        
        return f"{entity.value}-{code}"

async def generate_land_id(entity: CodeCounterEnum, project_name:str, desa_code:str) -> str:

    obj_current = await crud.code_counter.get_by_entity(entity=entity)

    code_counter = 1
    max_digit = 5  

    if obj_current is None:
        obj_in = CodeCounter(entity=entity, last=code_counter, digit=max_digit)
        await crud.code_counter.create(obj_in=obj_in)

        code = str(code_counter).zfill(max_digit)

        if CodeCounterEnum.LAND_BANK:
            year = datetime.today().year

            return f"{entity.value}-{year}-{project_name}-{desa_code}-{code}"
        
    else:
        code_counter = obj_current.last + 1
        max_digit = obj_current.digit or max_digit
        max_value = 10 ** max_digit - 1

        if code_counter > max_value:
            max_digit += 1  

        obj_new = CodeCounter(entity=obj_current.entity, last=code_counter, digit=max_digit)
        await crud.code_counter.update(obj_current=obj_current, obj_new=obj_new)

        code = str(code_counter).zfill(max_digit)

        if CodeCounterEnum.MEMO:
            year = datetime.today().year

            return f"{entity.value}-{year}-{project_name}-{desa_code}-{code}"
        
        return f"{entity.value}-{code}"