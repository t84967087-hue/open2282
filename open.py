from playwright.sync_api import sync_playwright, TimeoutError
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

def automate_redeploy_cycle():
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.firefox.launch(headless=Tr)
        context = browser.new_context()

        try:
            page = context.new_page()

            while True:  # Бесконечный цикл повторений
                logger.info("Начинаем новый цикл Redeploy...")

                # 1. Переход на сайт и вход в аккаунт
                logger.info("Открываем сайт")
                page.goto("https://vercel.com/login", timeout=60000)
                page.wait_for_load_state("domcontentloaded", timeout=10000)

                logger.info("Выполняем вход в аккаунт")

                # Ввод email и нажатие кнопки
                email_input = page.get_by_placeholder("Email Address")
                if not email_input.is_visible():
                    logger.error("Поле Email не найдено. Пропускаем цикл.")
                    logger.info("Ждём 46 минут до следующего запуска...")
                    time.sleep(2760)
                    continue  # Переходим к следующему циклу
                email_input.fill("t84967087@gmail.com")

                login_button = page.get_by_text("Continue with Email", exact=True)
                if not login_button.is_visible():
                    logger.error("Кнопка входа не найдена. Пропускаем цикл.")
                    logger.info("Ждём 46 минут до следующего запуска...")
                    time.sleep(2760)
                    continue
                login_button.click()
                page.wait_for_timeout(5000)

                # Ввод кода
                user_code = input("Введите код для подтверждения (или нажмите Enter, чтобы пропустить): ").strip()
                if not user_code:
                    logger.warning("Код не введён. Пропускаем цикл.")
                    logger.info("Ждём 46 минут до следующего запуска...")
                    time.sleep(2760)
                    continue

                visible_inputs = page.query_selector_all("input:visible")
                if not visible_inputs:
                    logger.error("Нет видимых полей ввода. Пропускаем цикл.")
                    logger.info("Ждём 46 минут до следующего запуска...")
                    time.sleep(2760)
                    continue

                leftmost_input = min(
                    visible_inputs,
                    key=lambda el: el.bounding_box()["x"] if el.bounding_box() else float("inf")
                )
                leftmost_input.fill(user_code)
                page.wait_for_timeout(3000)

                logger.info("Вход выполнен успешно")

                # 2. Ожидание 60 секунд после входа
                logger.info("Ожидание 60 секунд после входа...")
                time.sleep(60)

                # 3. Клик по первой кнопке Redeploy
                logger.info("Ищем первую кнопку Redeploy...")
                first_button = page.get_by_role("button", name="Redeploy")

                try:
                    first_button.wait_for(timeout=30000, state="visible")
                    first_button.click(force=True)
                    logger.info("Первая кнопка Redeploy кликнута!")
                except Exception as e:
                    logger.error(f"Первая кнопка Redeploy не найдена или недоступна: {e}")
                    logger.info("Пропускаем клик по первой кнопке, переходим к поиску второй кнопки...")

                # 4. Клик по второй кнопке в модальном окне
                logger.info("Ищем кнопку в модальном окне (data-testid='redeploy-modal/redeploy-button')...")
                second_button = page.locator('[data-testid="redeploy-modal/redeploy-button"]')

                try:
                    second_button.wait_for(timeout=30000, state="visible")
                    second_button.click(force=True)
                    logger.info("Кнопка в модальном окне кликнута!")
                except Exception as e:
                    logger.error(f"Не удалось кликнуть по кнопке в модальном окне: {e}")
                    # Диагностика
                    modal_buttons = page.locator('[data-testid^="redeploy-modal"]').all_inner_texts()
                    logger.info(f"Кнопки в модальном окне: {modal_buttons}")

                # 5. Успешное завершение цикла или пропуск
                logger.info("Цикл выполнен (частично или полностью). Ждём 46 минут до следующего запуска...")
                time.sleep(2760)

        except KeyboardInterrupt:
            logger.info("Программа остановлена пользователем.")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
        finally:
            # Закрытие браузера
            logger.info("Закрываем браузер")
            browser.close()

if __name__ == "__main__":
    automate_redeploy_cycle()
