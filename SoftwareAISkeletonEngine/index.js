
import { program } from 'commander';
import inquirer from 'inquirer';
import fs from 'fs-extra';
import path from 'path';
import { 
  appPy, 
  checkoutPaymentButton, 
  checkoutPaymentSelected, 
  loginAndRegister, 
  navigation_js, 
  landing_js, 
  script_base_login_js, 
  user_code_init_env, 
  docker_file, 
  docker_compose_file, 
  repo_file, 
  appcompany_file, 
  fb_file, 
  requirements_file, 
  build_file

 } from './themes/flask-web-product.js';




// Templates mapping
const themes = {
  'flask-web-product': {
    description: 'Flask web product with Checkout, Login, Dashboard',
    files: [
      { target: 'app.py', content: appPy},
      { target: 'Dockerfile', content: docker_file},
      { target: 'docker-compose.yml', content: docker_compose_file},
      { target: 'repo.json', content: repo_file},
      { target: 'build.py', content: build_file},
      { target: 'requirements.txt', content: requirements_file},
      { target: 'static/js/checkout-payment-button.js', content: checkoutPaymentButton },
      { target: 'static/js/checkout-payment-selected.js', content: checkoutPaymentSelected },
      { target: 'static/js/loginAndRegistrer.js', content: loginAndRegister },
      { target: 'static/js/navigation.js', content: navigation_js},
      { target: 'static/js/landing.js', content: landing_js},
      { target: 'Keys/keys.env', content: user_code_init_env},
      { target: 'Keys/appcompany.json', content: appcompany_file},
      { target: 'Keys/fb.py', content: fb_file},
    ],
    placeholders: ['index','login','dashboard','checkout','success']
  }
};

async function main() {

  // ——————————————
  // COMMAND: create-py-app
  // ——————————————
  program
    .name('create-py-app')
    .description('Scaffold Flask Python app with multiple themes')
    .version('1.2.0')
    .option('-t, --theme <theme>', 'Choose an application theme', 'flask-web-product');

  program
    .argument('<project-name>', 'Project folder name')
    .action(async (name, options) => {
      const { theme } = options;
      if (!themes[theme]) {
        console.error(`Unknown theme '${theme}'. Available: ${Object.keys(themes).join(', ')}`);
        process.exit(1);
      }

      const root = path.resolve(process.cwd(), name);
      if (await fs.pathExists(root)) {
        console.error(`Directory ${name} exists.`);
        process.exit(1);
      }

      // Create directories
      await fs.mkdirp(root);
      await fs.mkdirp(path.join(root, 'templates'));
      await fs.mkdirp(path.join(root, 'static/js'));
      await fs.mkdirp(path.join(root, 'static/css'));
      await fs.mkdirp(path.join(root, 'Keys'));

      const themeDef = themes[theme];

      // Write theme files
      for (const file of themeDef.files) {
        const targetPath = path.join(root, file.target);
        await fs.mkdirp(path.dirname(targetPath));
        await fs.writeFile(targetPath, file.content);
      }

      // Write placeholders
      themeDef.placeholders.forEach(page => {
        const tpl = path.join(root, 'templates', `${page}.html`);
        fs.writeFileSync(tpl, `<!-- ${page} for theme ${theme} -->`);
      });

      // Write README
      const readme = `# ${name}

Created with theme '${theme}': ${themeDef.description}
`;
      await fs.writeFile(path.join(root, 'README.md'), readme);

      console.log(`Project '${name}' created using theme '${theme}'.`);
    });



  // ——————————————
  // COMMAND: schedule-task
  // ——————————————
  program
    .command('schedule-task')
    .description('Agendar uma tarefa no servidor Flask/Celery')
    .requiredOption('-a, --agent <name>',     'nome do agente a ser executado')
    .requiredOption('-e, --email <email>',    'e-mail do usuário dono da tarefa')
    .requiredOption('-r, --runAt <datetime>', 'data e hora (ISO, ex: 2025-05-20T15:30:00)')
    .requiredOption('-g, --repo <url>',       'URL do repositório Git (repo_git)')
    .option('-p, --params <json>',            'JSON com parâmetros adicionais', '{}')
    .action(async (opts) => {
      const API_BASE = process.env.SCHEDULER_API_URL || 'http://localhost:5100';

      // validação de data
      const dt = moment.tz(opts.runAt, 'America/Sao_Paulo');
      if (!dt.isValid()) {
        console.error('❌ Data inválida! Use ISO, ex: 2025-05-20T15:30:00');
        process.exit(1);
      }

      // parse dos params extras
      let extraParams;
      try {
        extraParams = JSON.parse(opts.params);
      } catch {
        console.error('❌ Parâmetros inválidos: --params deve ser JSON.');
        process.exit(1);
      }

      // monta payload
      const payload = {
        agent:    opts.agent,
        run_at:   dt.format(),           // ex: "2025-05-20T15:30:00-03:00"
        repo_git: opts.repo,
        params:   { user_email: opts.email, ...extraParams }
      };

      console.log('⏳ Enviando requisição...', payload);
      try {
        const res = await axios.post(`${API_BASE}/schedule-agent`, payload);
        console.log('✅ Agendado com sucesso!');
        console.log('  • db_task_id:    ', res.data.db_task_id);
        console.log('  • celery_task_id:', res.data.celery_task_id);
        console.log('  • scheduled_for: ', res.data.scheduled_for);
      } catch (err) {
        console.error('❌ Erro ao agendar:', err.response?.data || err.message);
        process.exit(1);
      }
    });

  await program.parseAsync();
}


main();
