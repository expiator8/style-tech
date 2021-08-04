import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from django.utils import timezone


emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+",
    flags=re.UNICODE,
)


def scroll_down(browser, action, to):
    last_height = browser.execute_script("return document.body.scrollHeight")
    action.move_to_element(to).perform()
    new_height = browser.execute_script("return document.body.scrollHeight")
    if last_height != new_height:
        scroll_down(action, to)


def get_table(browser, action, m_page):
    if m_page != 0:
        next_page = browser.find_element_by_class_name("pagination_next__1ITTf")
        browser.execute_script("arguments[0].click();", next_page)
        time.sleep(3)
        table = browser.find_elements_by_class_name("basicList_item__2XT81")
        return table
    to = browser.find_element_by_class_name("pagination_num__-IkyP")
    scroll_down(browser, action, to)
    table = browser.find_elements_by_class_name("basicList_item__2XT81")
    return table


def extract_standard_review(browser, results, page_num):
    results = results
    reviews_info = browser.find_element_by_class_name(
        "reviewItems_list_review__1sgcJ"
    ).find_elements_by_tag_name("li")
    now = datetime.datetime.now().date()
    for review_info in reviews_info:
        info = review_info.find_element_by_class_name("reviewItems_etc_area__2P8i3")
        rating = info.find_element_by_class_name(
            "reviewItems_average__16Ya-"
        ).text.replace("평점", "")
        date_buy = info.find_elements_by_class_name("reviewItems_etc__1YqVF")
        buy = date_buy[0].text
        date = date_buy[2].text[:-1].split(".")
        try:
            if date[1][0] == "0":
                date[1] = date[1][1]
            if date[2][0] == "0":
                date[2] = date[2][1]
        except IndexError:
            pass
        date_info = datetime.date(2000 + int(date[0]), int(date[1]), int(date[2]))
        date_range = datetime.timedelta(days=30)
        if now - date_info <= date_range:
            review = emoji_pattern.sub(
                r"",
                review_info.find_element_by_class_name(
                    "reviewItems_text__XIsTc"
                ).text.replace("\n", ""),
            )

            result = {
                "review": review,
                "rating": int(rating),
                "date_created": date,
                "buy": buy,
            }
            results.append(result)
        else:
            return results

    try:
        next_page = browser.find_elements_by_class_name("pagination_pagination__2M9a4")[
            1
        ].find_elements_by_tag_name("a")
        if page_num > 10:
            page_num = 1
        if page_num % 10 == 1:
            next_page = next_page[page_num]
        if page_num % 10 == 2:
            next_page = next_page[page_num]
        if page_num % 10 == 3:
            next_page = next_page[page_num]
        if page_num % 10 == 4:
            next_page = next_page[page_num]
        if page_num % 10 == 5:
            next_page = next_page[page_num]
        if page_num % 10 == 6:
            next_page = next_page[page_num]
        if page_num % 10 == 7:
            next_page = next_page[page_num]
        if page_num % 10 == 8:
            next_page = next_page[page_num]
        if page_num % 10 == 9:
            next_page = next_page[page_num]
        if page_num % 10 == 0:
            next_page = next_page[page_num]
        next_page.click()
        time.sleep(1)
        page_num += 1
        extract_standard_review(browser, results, page_num)
    except Exception:
        return results


def extract_store_review(browser, results, page_num):
    results = results
    reviews_info = browser.find_element_by_class_name(
        "TsOLil1PRz"
    ).find_elements_by_tag_name("li")
    now = datetime.datetime.now().date()
    for review_info in reviews_info:
        rating = review_info.find_element_by_class_name("_15NU42F3kT").text
        date = (
            review_info.find_element_by_class_name("_2FmJXrTVEX")
            .find_element_by_tag_name("span")
            .text[:-1]
            .split(".")
        )
        try:
            if date[1][0] == "0":
                date[1] = date[1][1]
            if date[2][0] == "0":
                date[2] = date[2][1]
        except IndexError:
            pass
        date_info = datetime.date(2000 + int(date[0]), int(date[1]), int(date[2]))
        date_range = datetime.timedelta(days=3)
        if now - date_info <= date_range:
            review = emoji_pattern.sub(
                r"",
                review_info.find_element_by_class_name("YEtwtZFLDz")
                .find_element_by_class_name("_3QDEeS6NLn")
                .text.replace("\n", ""),
            )
            result = {
                "review": review,
                "rating": int(rating),
                "date_created": date,
                "buy": None,
            }
            results.append(result)
        else:
            return results

    try:
        next_page = browser.find_element_by_class_name(
            "_1HJarNZHiI  "
        ).find_elements_by_tag_name("a")
        if page_num > 11:
            page_num = 1
        if page_num % 10 == 1:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 2:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 3:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 4:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 5:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 6:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 7:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 8:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 9:
            next_page = next_page[page_num + 1]
        if page_num % 10 == 0:
            next_page = next_page[page_num + 1]
        browser.execute_script("arguments[0].click();", next_page)
        time.sleep(1)
        page_num += 1
        extract_store_review(browser, results, page_num)
    except Exception:
        return results


def extract_info(browser, t):
    if "ad" not in t.get_attribute("class"):
        url_info = t.find_element_by_class_name("basicList_title__3P9Q7")
        url_info = url_info.find_element_by_tag_name("a")
        url = url_info.get_property("href")

        title = url_info.text

        categories_info = t.find_element_by_class_name("basicList_depth__2QIie")
        categories_info = categories_info.find_elements_by_tag_name("a")
        categories = []
        for c in categories_info:
            category = c.text
            categories.append(category)

        num_zzim = (
            t.find_element_by_class_name("basicList_btn_zzim__2MGkM")
            .text.replace("찜하기", "")
            .replace(",", "")
        )
        if "만" in num_zzim:
            num_zzim = num_zzim.replace(".", "").replace("만", "")
            num_zzim = num_zzim + "000"
        try:
            sellers = []
            seller = t.find_element_by_class_name("basicList_mall__sbVax").text
            sellers.append(seller)
        except Exception:
            pass

        registration = t.find_element_by_class_name(
            "basicList_etc_box__1Jzg6"
        ).find_elements_by_tag_name("span")
        registration = registration[0].text.replace("등록일 ", "")[:-1].split(".")
        try:
            if registration[1][0] == "0":
                registration[1] = registration[1][1]

        except IndexError:
            pass

        try:
            over_sea_delivery = t.find_element_by_class_name("ad_label__Ve7Bp")
            over_sea_delivery = True
            title = title.replace("해외", "", 1)
        except Exception:
            over_sea_delivery = False

        now = timezone.localtime().strftime("%M%S")
        photo = t.find_element_by_class_name("thumbnail_thumb_wrap__1pEkS")
        photo_name = f"Naver_{title[len(title)-1]}_{now}"
        photo = photo.screenshot(f"uploads/naver_photos/{photo_name}.png")

        url_info.click()
        browser.switch_to.window(browser.window_handles[1])
        try:
            price = browser.find_element_by_class_name(
                "lowestPrice_num__3AlQ-"
            ).text.replace(",", "")

            info = browser.find_elements_by_class_name("top_info_inner__1cEYE")
            first_info = info[0].find_elements_by_tag_name("span")
            for f in first_info:
                if "top_brand__1Q2zO" not in f.get_attribute("class"):
                    f = f.text
                    if "제조사" in f:
                        manufacturer = f.replace("제조사 ", "")

                    if "브랜드" in f:
                        brand = f.replace("브랜드 ", "")

                    if "등록일" in f:
                        registration = f.replace("등록일 ", "")[:-1].split(".")
                        if registration[1][0] == "0":
                            registration[1] = registration[1][1]

            try:
                second_info = info[1].find_elements_by_tag_name("span")
                if second_info:
                    for s in second_info:
                        s = s.text.replace(" ", "")
                        if "발목높이" in s:
                            ankle_height = s.replace("발목높이:", "")
                        if "굽높이" in s:
                            heel_height_info = s.replace("굽높이:", "")
                            if "," in heel_height_info:
                                heel_height = heel_height_info.split(",")
                            else:
                                heel_height = []
                                heel_height.append(heel_height_info)
                        if "주요특징" in s:
                            feature_info = s.replace("주요특징:", "")
                            if "," in feature_info:
                                feature = feature_info.split(",")
                            else:
                                feature = []
                                feature.append(feature_info)
                        if "주요소재(신발)" in s:
                            main_material_info = s.replace("주요소재(신발):", "")
                            if "," in main_material_info:
                                main_material = main_material_info.split(",")
                            else:
                                main_material = []
                                main_material.append(main_material_info)
                        if "부가기능" in s and "해당없음" not in s:
                            add_ons_info = s.replace("부가기능:", "")
                            if "," in add_ons_info:
                                add_ons = add_ons_info.split(",")
                            else:
                                add_ons = []
                                add_ons.append(add_ons_info)
                        if "솔:" in s:
                            sole_material = s.replace("솔:", "")
                        if "성별" in s:
                            gender = s.replace("성별:", "")

            except Exception:
                pass

            sellers_info = browser.find_elements_by_class_name(
                "productByMall_text_over__1rkUg"
            )
            sellers = []
            for seller in sellers_info:
                try:
                    seller = seller.find_element_by_tag_name("img").get_property("alt")
                    sellers.append(seller)
                except Exception:
                    seller = seller.find_element_by_tag_name("a").text
                    sellers.append(seller)

            results = []
            page_num = 1
            try:
                ordered_newest = browser.find_element_by_class_name(
                    "filter_sort_box__223qy"
                ).find_elements_by_class_name("filter_sort__1YUTp")[1]
                browser.execute_script("arguments[0].click();", ordered_newest)
                time.sleep(2)
                naver_reviews = extract_standard_review(results, page_num)
            except Exception:
                naver_reviews = None

        except Exception:
            price = browser.find_element_by_class_name("aICRqgP9zw")
            price = price.find_element_by_class_name("_1LY7DqCnwR").text.replace(
                ",", ""
            )
            kind = browser.find_elements_by_class_name("_1iuv6pLHMD")[:14]
            info = browser.find_elements_by_class_name("ABROiEshTD")[:14]

            for index, i in enumerate(kind):
                info_text = info[index].text.replace(" ", "")
                if "상품상세참조" not in info_text and "해당사항없음" not in info_text:
                    if "제조사" in i.text:
                        manufacturer = info_text
                    if "브랜드" in i.text:
                        brand = info_text
                    if "발목높이" in i.text:
                        ankle_height = info_text
                    if "굽높이" in i.text:
                        heel_height_info = info_text
                        if "," in heel_height_info:
                            heel_height = heel_height_info.split(",")
                        else:
                            heel_height = []
                            heel_height.append(heel_height_info)
                    if "주요소재(신발)" in i.text:
                        main_material_info = info_text
                        if "," in main_material_info:
                            main_material = main_material_info.split(",")
                        else:
                            main_material = []
                            main_material.append(main_material_info)
                    if "부가기능" in i.text and "해당없음" not in info_text:
                        add_ons_info = info_text
                        if "," in add_ons_info:
                            add_ons = add_ons_info.split(",")
                        else:
                            add_ons = []
                            add_ons.append(add_ons_info)
                    if "솔" in i.text:
                        sole_material = info_text
                    if "성별" in i.text:
                        gender = info_text
                    if "주요특징" in i.text:
                        feature_info = info_text
                        if "," in feature_info:
                            feature = feature_info.split(",")
                        else:
                            feature = []
                            feature.append(feature_info)
            results = []
            page_num = 1
            try:
                ordered_newest = (
                    browser.find_element_by_class_name("EP5-YthxnX")
                    .find_elements_by_class_name("_1K9yWX-Lpq")[1]
                    .find_element_by_tag_name("a")
                )
                browser.execute_script("arguments[0].click();", ordered_newest)
                time.sleep(2)
                naver_reviews = extract_store_review(results, page_num)
            except Exception:
                naver_reviews = None

        if "ankle_height" not in locals():
            ankle_height = None
        if "heel_height" not in locals():
            heel_height = None
        if "feature" not in locals():
            feature = None
        if "main_material" not in locals():
            main_material = None
        if "add_ons" not in locals():
            add_ons = None
        if "sole_material" not in locals():
            sole_material = None
        if "gender" not in locals():
            gender = None
        if "brand" not in locals():
            brand = None
        if "manufacturer" not in locals():
            manufacturer = None
        if "sellers" not in locals():
            sellers = None
        if "categories" not in locals():
            categories = None

        browser.close()
        browser.switch_to.window(browser.window_handles[0])

        time.sleep(1)

        return {
            "title": title,
            "price": int(price),
            "url": url,
            "photo": photo_name,
            "brand": brand,
            "manufacturer": manufacturer,
            "registration": registration,
            "over_sea_delivery": bool(over_sea_delivery),
            "sellers": sellers,
            "categories": categories,
            "ankle_height": ankle_height,
            "heel_height": heel_height,
            "feature": feature,
            "main_material": main_material,
            "add_ons": add_ons,
            "sole_material": sole_material,
            "gender": gender,
            "dibs": int(num_zzim),
            "reviews": naver_reviews,
        }


def get_info(browser, table):
    info = []
    for t in table:
        result = extract_info(browser, t)
        if result:
            info.append(result)
    return info


def get_naver_result(url, max_page):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    results = []
    browser.get(url)
    action = ActionChains(browser)
    for m_page in range(max_page):
        try:
            table = get_table(browser, action, m_page)
            info = get_info(browser, table)
            results = results + info
        except Exception:
            pass
    return results
