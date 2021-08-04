import os
import random
from django.core.files import File
import time
import datetime
import re
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from django.core.management.base import BaseCommand
from instagram_products import models as instagram_product_models
from instagram_reviews import models as instagram_review_models
from instagram_users import models as instagram_user_models


# 검색할 태그 키워드
TAGS_LIST = ["운동화"]
# 검색할 인플루언서 키워드
INFLUENCER_LIST = ["hi_bambigirl", "effectivewear"]
# 광고라고 판단할 태그
AD_TAGS_LIST = ["#협찬", "#광고"]

# 인스타그램 홈 Url
base_url = os.environ.get("BASE_URL")
# 인스타그램 태그로 검색 후 Url
url_searched = base_url + os.environ.get("URL_SEARCHED")
# 인스타그램 로그인 정보
id = os.environ.get("INSTAGRAM_USERNAME")
pw = os.environ.get("INSTAGRAM_PASSWORD")
# 리뷰 텍스트에서 제거할 정보(이모티콘, 심볼 등)
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+",
    flags=re.UNICODE,
)


def save_writer(user_id, obj, is_influencer, influencer_info):

    """
    instagram_products.InstagramProduct,
    instagram_reviews.InstagramReview
    의 writer 값을 저장
    :param user_id: integer(primary key of Instagram User Model)
    :param is_influencer: boolean(True or False)
    :param influencer_info: dict
    """

    try:
        writer = instagram_user_models.InstagramUser.objects.get(insta_id=user_id)
    except Exception:
        writer = instagram_user_models.InstagramUser(insta_id=user_id)
        writer.save()
        pk = writer.pk
        writer = instagram_user_models.InstagramUser.objects.get(pk=pk)
    writer.is_influencer = is_influencer
    writer.followers = influencer_info["followers"]
    writer.followings = influencer_info["followings"]
    writer.save()
    obj.writer = writer
    obj.save()


def save_img(url, insta_product, searched_keyword, date_created):

    """
    instagram_products.InstagramPhoto의 file 값을 저장
    :param url: string(image src)
    :param insta_product: object(instagram_products.InstagramProduct)
    :param searched_keyword: string
    :param date_created: datetime
    """

    insta_photo = instagram_product_models.InstagramPhoto(
        instagram_product=insta_product,
    )
    photo_name = f"Insta_{searched_keyword}_{str(date_created)}_{insta_photo.pk}.png"
    result = urlretrieve(url)
    insta_photo.file.save(
        os.path.basename(photo_name),
        File(open(result[0], "rb")),
    )
    insta_photo.save()


def save_info(post, searched_keyword, influencer_info):

    """
    게시물 데이터 db 저장
    :param post: dict
    :param searched_keyword: string
    :param influencer_info: dict
    """

    main = post["details"][0]
    reviews = post["details"][1:]
    date_created = main["date_created"]
    text = main["text"]
    writer = main["writer"]
    likes = post["likes"]
    visits = post["visits"]
    url = post["url"]
    img_url = post["img_url"]
    instagram_hash_tags = post["tags"]
    is_influencer = main["is_influencer"]
    try:
        product = instagram_product_models.InstagramProduct.objects.get(url=url)
        product.date_created = date_created
        product.text = text
        product.likes = likes
        product.visits = visits
        save_writer(writer, product, is_influencer, influencer_info)
    except Exception:
        product = instagram_product_models.InstagramProduct(
            date_created=date_created,
            text=text,
            likes=likes,
            visits=visits,
            url=url,
            is_ad=False,
        )
        save_writer(writer, product, is_influencer, influencer_info)
        pk = product.pk
        product = instagram_product_models.InstagramProduct.objects.get(pk=pk)
        for u in img_url:
            save_img(u, product, searched_keyword, date_created)
    if reviews:
        for review in reviews:
            text_review = review["text"]
            likes_review = review["likes"]
            writer_review = review["writer"]
            date_created_review = review["date_created"]
            is_influencer = review["is_influencer"]
            filter_args = {}
            filter_args["text__exact"] = text_review
            filter_args["instagram_product__url__exact"] = url
            filter_args["writer__insta_id__exact"] = writer_review
            filter_args["date_created__exact"] = date_created_review
            review_exist = instagram_review_models.InstagramReview.objects.filter(
                **filter_args
            )
            if not review_exist:
                if text_review != "":
                    review = instagram_review_models.InstagramReview(
                        likes=likes_review,
                        date_created=date_created_review,
                        text=text_review,
                        instagram_product=product,
                    )
                    save_writer(writer_review, review, is_influencer, influencer_info)
    try:
        search_keyword = instagram_product_models.SearchedKeyword.objects.get(
            name=searched_keyword
        )
    except Exception:
        search_keyword = instagram_product_models.SearchedKeyword.objects.create(
            name=searched_keyword
        )
    product.searched_keywords.add(search_keyword)
    if instagram_hash_tags:
        for instagram_hash_tag in instagram_hash_tags:
            if instagram_hash_tag in AD_TAGS_LIST:
                product.is_ad = True
                product.save()
            try:
                instagram_hash_tag = (
                    instagram_product_models.InstagramHashTag.objects.get(
                        name=instagram_hash_tag
                    )
                )
            except Exception:
                instagram_hash_tag = (
                    instagram_product_models.InstagramHashTag.objects.create(
                        name=instagram_hash_tag
                    )
                )
            product.instagram_hash_tags.add(instagram_hash_tag)


def get_soup_elements_by_class(browser, tag, class_name, wait=0):

    """
    tags by class_name의 bs4.BeautifulSoup 및 bs4.element.ResultSet 생성
    :param browser: selenium driver
    :param tag: string
    :param class_name: string
    :return: bs4.BeautifulSoup, bs4.element.ResultSet as tuple
    """

    html = browser.execute_script("return document.documentElement.outerHTML;")
    soup = BeautifulSoup(html, "lxml")
    elements = soup.find_all(tag, {"class": class_name})
    time.sleep(random.randint(1, 2))
    return soup, elements


def open_more_review_btn(browser):

    """
    게시물의 리뷰 더보기 버튼 클릭
    :param browser: selenium driver
    """

    more = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "dCJp8"))
    )
    more.click()
    time.sleep(random.randint(1, 2))


def get_post_soup(browser, text_length=0):

    """
    게시물의 bs4.BeautifulSoup 및 bs4.element.ResultSet 생성
    :param browser: selenium driver
    :param text_length: integer
    :return: bs4.BeautifulSoup, bs4.element.ResultSet as tuple
    """

    try:
        open_more_review_btn(browser)
        reviews_info = get_soup_elements_by_class(browser, "div", "C4VMK")
        t_length = len(reviews_info[1])
        if t_length == text_length:
            return reviews_info
        reviews_info = get_post_soup(browser, t_length)
    except Exception:
        reviews_info = get_soup_elements_by_class(browser, "div", "C4VMK")
    return reviews_info


def get_next_image_url(browser, arr, count):

    """
    게시물의 모든 image url 생성
    :param browser: selenium driver
    :param arr: array
    :param count: integer
    :return: image url as array
    """

    try:
        img_info = get_soup_elements_by_class(browser, "div", "ZyFrc")
        url = img_info[1][count].find("img", {"class": "FFVAD"})["src"]
        arr.append(url)
        browser.find_element_by_class_name("coreSpriteRightChevron").click()
        time.sleep(random.uniform(1.0, 1.3))
        count = 1
        arr = get_next_image_url(browser, arr, count)
    except Exception:
        pass
    return arr


def scroll_down(browser):

    """
    페이지 스크롤 내리기
    :param browser: selenium driver
    """

    body = browser.find_element_by_css_selector("body")
    body.send_keys(Keys.PAGE_UP)
    time.sleep(random.randint(1, 2))
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.randint(1, 2))
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random.randint(5, 6))


def extract_info(browser, table, now, interval, date_format, is_popular, check):

    """
    게시물의 전체 정보 스크래핑
    :param browser: selenium driver
    :param table: bs4.element.Tag
    :param now: datetime
    :param interval: datetime
    :param date_format: string
    :param is_popular: boolean(True or False)
    :param check: boolean(True or False)
    :return: a post information as array
    """

    result = {}
    current_table = browser.find_element_by_xpath('//a[@href="' + table + '"]')
    current_table.click()
    url_detail = base_url + table
    post_info = get_post_soup(browser)
    if post_info:
        soup = post_info[0]
        likes_info = soup.find("div", {"class": "Nm9Fw"})
        visits = soup.find("span", {"class": "vcOH2"})
        text_info = post_info[1]
        post_created = soup.find("time", {"class": "_1o9PC"})
        post_created = post_created["datetime"]
        post_created = datetime.datetime.strptime(post_created, date_format)
        if not check:
            if now >= post_created and interval <= post_created or is_popular:
                try:
                    try:
                        likes = likes_info.find("a", {"class": "zV_Nj"})
                        try:
                            likes = int(likes.find("span").getText().replace(",", ""))
                        except Exception:
                            likes = int(
                                likes.getText()
                                .replace(",", "")
                                .replace("좋아요 ", "")
                                .replace("개", "")
                            )
                        visits = 0
                    except Exception:
                        try:
                            visits = int(visits.find("span").getText().replace(",", ""))
                        except Exception:
                            visits = int(
                                visits.getText()
                                .replace(",", "")
                                .replace("조회 ", "")
                                .replace("회", "")
                            )
                        likes = 0
                except Exception:
                    likes = 0
                    visits = 0
                img_results = []
                img_results = get_next_image_url(browser, img_results, 0)
                if not img_results:
                    url = current_table.find_element_by_class_name(
                        "FFVAD"
                    ).get_attribute("src")
                    img_results.append(url)
                time.sleep(5)
                tag_results = []
                if len(text_info) >= 2:
                    text_count = 2
                else:
                    text_count = 1
                for t_info in text_info[:text_count]:
                    tags_info = t_info.find_all("a", {"class": "xil3i"})
                    if tags_info:
                        for tag in tags_info:
                            tag_results.append(tag.getText())
                detail_results = []
                for t in text_info:
                    detail_info = {}
                    writer = t.find(
                        "a", {"class": "sqdOP yWX7d _8A5w5 ZIAjV"}
                    ).getText()
                    text = emoji_pattern.sub(
                        r"", t.find("span", recursive=False).getText().replace("\n", "")
                    )
                    date_created = t.find("time", {"class": "FH9sR"})["datetime"]
                    date_created = datetime.datetime.strptime(date_created, date_format)
                    likes_review = t.find("button", {"class": "FH9sR"})
                    if likes_review and "좋아요" in likes_review.getText():
                        likes_review = int(
                            likes_review.getText().replace("좋아요 ", "").replace("개", "")
                        )
                    else:
                        likes_review = 0

                    if writer in INFLUENCER_LIST:
                        detail_info["is_influencer"] = True
                    else:
                        detail_info["is_influencer"] = False
                    detail_info["writer"] = writer
                    detail_info["text"] = text
                    detail_info["date_created"] = date_created
                    detail_info["likes"] = likes_review
                    detail_results.append(detail_info)
                result["url"] = url_detail
                result["img_url"] = img_results
                result["tags"] = tag_results
                result["date"] = post_created
                result["visits"] = visits
                result["likes"] = likes
                result["details"] = detail_results
        else:
            if interval > post_created:
                result = False
            else:
                result = True
    else:
        result = "error"
    xpath = "/html/body/div[5]/div[3]/button"
    browser.find_element_by_xpath(xpath).click()
    time.sleep(random.randint(1, 2))
    return result


def get_info(browser, table, popular=False, check_last=False):

    """
    게시물의 전체 정보 생성
    :param browser: selenium driver
    :param table: bs4.element.ResultSet
    :param popular: boolean(True or False)
    :param check_last: boolean(True or False)
    :return: posts information as array
    """

    info = []
    now = datetime.datetime.now() - datetime.timedelta(hours=9)
    scrape_to = now - datetime.timedelta(hours=1)
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    time.sleep(1)
    for t in table:
        result = extract_info(
            browser, t, now, scrape_to, date_format, popular, check_last
        )
        if not result:
            return info
        if result and result != "error":
            info.append(result)
    return info


def get_table(browser, keyword, influencer, t):

    """
    스크래핑을 수행할 게시물의 url path 생성
    :param browser: selenium driver
    :param keyword: string
    :param influencer: boolean(True or False)
    :param t: array
    :return: lxml soup and url path as tuple
    """

    table_info = get_soup_elements_by_class(browser, "div", "v1Nh3", 20)
    for i in table_info[1]:
        if i.a["href"] not in t:
            t.append(i.a["href"])
    if not influencer:
        last_table = t[-1:]
        is_last = get_info(browser, last_table, check_last=True)
        if not is_last:
            return table_info[0], t[:-1]
        elif is_last == "empty":
            table = get_table(browser, keyword, influencer, t)
        else:
            for i in range(2):
                browser.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(0.2, 0.3))
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(random.uniform(0.2, 0.3))
            table = get_table(browser, keyword, influencer, t)
        return table
    else:
        return table_info[0], t[:-1]


def show_scrape_log(self, key, count, type):

    """
    스크래핑 log를 console에 출력
    :param self: Command
    :param key: string
    :param count: integer
    :param type: string
    """

    self.stdout.write(self.style.SUCCESS(f"{key} {count}EA {type} created!"))


def save_instagram_results(self, insta_results):

    """
    전체 크롤링 log를 console에 출력
    :param insta_results: array
    """

    total_popular_count = 0
    total_recent_count = 0
    for result in insta_results:
        product_count_popular = 0
        product_count_recent = 0
        keyword = result["searched"]
        influencer = result["influencer"]
        is_influencer = influencer["is_influencer"]
        for p in result["post_popular"]:
            save_info(p, keyword, influencer)
            product_count_popular = product_count_popular + 1
        for r in result["post_recent"]:
            save_info(r, keyword, influencer)
            product_count_recent = product_count_recent + 1
        total_popular_count = total_popular_count + product_count_popular
        total_recent_count = total_recent_count + product_count_recent
        log_str = ["(popular)", "(recent)", "total", "(all)"]
        if is_influencer:
            show_scrape_log(self, keyword, product_count_popular, log_str[1])
        else:
            show_scrape_log(self, keyword, product_count_popular, log_str[0])
            show_scrape_log(self, keyword, product_count_recent, log_str[1])
    total_count = total_popular_count + total_recent_count
    if is_influencer:
        show_scrape_log(self, log_str[2], total_popular_count, log_str[1])
    else:
        show_scrape_log(self, log_str[2], total_popular_count, log_str[0])
        show_scrape_log(self, log_str[2], total_recent_count, log_str[1])
    show_scrape_log(self, log_str[2], total_count, log_str[3])


def instagram_login(browser):

    """
    인스타그램 로그인
    :param browser: selenium driver
    """

    login_info = browser.find_elements_by_tag_name("input")
    id_input = login_info[0]
    pw_input = login_info[1]
    id_input.send_keys(id)
    pw_input.send_keys(pw)
    pw_input.send_keys(Keys.RETURN)
    time.sleep(5)


def get_instagram_results(search_lists):

    """
    스크래핑 전체 정보 생성
    :param search_lists: array
    :return: whole scraping result as array
    """

    results = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(base_url)
    time.sleep(2)
    instagram_login(browser)
    if search_lists == TAGS_LIST:
        search_url_base = url_searched
        is_influencer = False
    else:
        search_url_base = base_url
        is_influencer = True
    for s in search_lists:
        result = {}
        table = []
        search_url = search_url_base + quote_plus(s)
        browser.get(search_url)
        time.sleep(10)
        table = get_table(browser, s, is_influencer, table)
        influencer = {}
        influencer["is_influencer"] = is_influencer
        if is_influencer:
            i_info = table[0].find_all("span", {"class": "g47SY"})
            followers = int(i_info[1]["title"].replace(",", ""))
            followings = int(i_info[2].getText().replace(",", ""))
            influencer["followers"] = followers
            influencer["followings"] = followings
        else:
            influencer["followers"] = 0
            influencer["followings"] = 0
        post_popular = table[1][:9]
        post_recent = table[1][9:]
        result["influencer"] = influencer
        result["searched"] = s
        browser.execute_script("window.scrollTo(0, 0);")
        result["post_popular"] = get_info(browser, post_popular, True)
        result["post_recent"] = get_info(browser, post_recent)
        results.append(result)
    browser.close()
    return results


class Command(BaseCommand):

    help = "This command scrape Instagram Products"

    def handle(self, *args, **options):

        get_influencer_results = get_instagram_results(INFLUENCER_LIST)
        save_instagram_results(self, get_influencer_results)
        get_tags_results = get_instagram_results(TAGS_LIST)
        save_instagram_results(self, get_tags_results)
