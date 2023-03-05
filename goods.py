import asyncio
import logging
from aiogram.types import Message, InputMediaPhoto
from goods_utils import get_product_from_db



async def find_goods(msg: Message):
    res_dict = get_product_from_db(msg.text) 
    res_list = ''
    media_group = []
    if len(res_dict) > 0:
        if len(res_dict) <= 5:
            for el in res_dict:
                res_string = str(el[7]) + '\n' + el[2] + '\n' + el[1] + '\n' + str(el[3]) + '\n' + str(el[4])
                # await msg.answer(res_string)
                i = 0
                if el[5]:
                    urls = el[5].split(', ')
                    cap = res_string
                    for url in urls:
                        if i < 2:
                            if cap:
                                photo=InputMediaPhoto(type='photo', media = 'https://b2b.i-t-p.pro/'+url+'?size=original', caption = cap)
                                cap = ''
                            else:
                                photo=InputMediaPhoto(type='photo', media = 'https://b2b.i-t-p.pro/'+url+'?size=original')
                            media_group.append(photo)
                            i+=1
                    await msg.answer_media_group(media=media_group)
                else:
                    await msg.answer(res_string)
        elif len(res_dict) > 5 and len(res_dict) <= 20:
            for el in res_dict:
                res_list = f"<b>{str(el[7])}</b>\n{el[2]}\n<a href=\"https://www.yandex.ru/search/?lr=213&offline_search=1&text={el[1].replace('<','').replace('>','')}\">{el[1].replace('<','').replace('>','')}</a>\n{str(el[3])}\n{str(el[4])}"
                await msg.reply(res_list, parse_mode="HTML")
        else:
            res_list = f"<b>Слишком много вариантов - {str(len(res_dict))}, уточните запрос</b>"
            await msg.reply(res_list, parse_mode="HTML")
    else:
        res_list = 'Ничего не найдено, перефразируйте запрос'
        await msg.reply(res_list, parse_mode="HTML")
